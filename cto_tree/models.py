# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.db import models

from corelib.consts import STATUS_NORMAL, STATUS_DELETE, FROM_SELF, FROM_CHILD, FROM_GRANDCHILD


class Trade(models.Model):
    # cto id
    cid = models.IntegerField()
    amount = models.FloatField()
    create_time = models.DateTimeField()

    @classmethod
    def create(cls, cid, amount):
        return cls.objects.create(cid=cid, amount=amount, create_time=datetime.now())


class Account(models.Model):
    create_time = models.DateTimeField()
    cid = models.IntegerField()
    amount = models.FloatField()
    source = models.IntegerField() #0, self, 1, child, 2, grandchild


    @classmethod
    def create(cls, cid, amount, source):
        return cls.objects.create(cid=cid, amount=amount, source=source, create_time=datetime.now())


class CTONode(models.Model):
    value = models.IntegerField()
    status = models.IntegerField(default=STATUS_NORMAL)
    name = models.CharField(max_length=50)
    parent_id = models.IntegerField(null=True, blank=True)
    root_id = models.IntegerField(null=True, blank=True)
    children_ids = models.CharField(max_length=3000)
    create_time = models.DateTimeField()
    balance = models.FloatField(default=0)


    class Meta:
        pass


    def income(self, amount, source=FROM_SELF):
        self.balance += amount
        self.save()
        Account.create(self.id, amount, source)
        # 底层节点更新父和祖父, 不需要父和祖父再向上更新.
        if source != FROM_SELF:
            return
        # 记录交易, 只在第一个节点记录, 不向上
        Trade.create(self.id, amount)
        # 前3个月
        if (datetime.now() - self.create_time).days > 90:
            return

        if self.parent_id is not None:
            parent = self.get_parent()
            parent_rate = 0.2 #TODO
            grandparent_rate = 0.1 #TODO
            parent.income(amount * parent_rate, source=FROM_CHILD)
            if parent.parent_id is not None:
                grandparent = parent.get_parent()
                grandparent.income(amount * grandparent_rate, source=FROM_GRANDCHILD)

    def get_parent(self):
        return CTONode.get(self.parent_id)

    @classmethod
    def get(cls, nid):
        try:
            return cls.objects.get(id=int(nid))
        except cls.DoesNotExist:
            raise "id %f does not exists" % nid

    @classmethod
    def create(cls, parent_id, name, value=0):
        node = cls.objects.create(parent_id=parent_id, name=name, value=value, create_time=datetime.now())
        node.notify_parent_by_add()
        node.root_id = node.parent.root_id if node.parent_id else None
        node.save()
        return node

    def notify_parent_by_add(self):
        if not self.parent_id:
            return
        parent = self.get(self.parent_id)
        self.parent = parent
        parent.add_new_child(self.id)

    def notify_parent_by_discard(self):
        parent = self.get(self.parent_id)
        parent.remove_child(self.id)

    def add_new_child(self, chid):
        self.children_ids = ','.join([self.children_ids, str(chid)]) if self.children_ids else str(chid)
        self.save()

    def remove_child(self, chid):
        chids = self.children_ids.split(',')
        try:
            chids.remove(str(chid))
            self.children_ids = ','.join(chids)
            self.save()
        except ValueError:
            raise 'does not have chid id %d' % chid

    def discard(self):
        self.notify_parent_by_discard()
        self.status = STATUS_DELETE
        self.save()
        for chid in self.children_ids:
            child = CTONode.get(chid)
            child.discard()

    def get_info(self):
        today = datetime.today()
        last_month_bgn = today - timedelta(days=1)#datetime(today.year, today.month-1, 1) if today.month > 1 else datetime(today.year-1, 12, 1)
        last_month_end = today+timedelta(days=1)#datetime(today.year, today.month, 1)
        return dict(
            id=self.id,
            status=self.status,
            parent_id=self.parent_id,
            children=map(int, self.children_ids.split(',')) if self.children_ids else [],
            grandchild = 'grand',
            name=self.name,
            balance=self.balance,
            create_time=self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            money_earned_last_month=sum([
                a.amount for a in Account.objects.filter(
                    cid=self.id, create_time__gte=last_month_bgn, create_time__lt=last_month_end
                )
            ]),
            money_earned_by_child_nodes_last_month=sum([
                a.amount for a in Account.objects.filter(
                    cid=self.id, create_time__gte=last_month_bgn,
                    create_time__lt=last_month_end, source=FROM_CHILD
                )
            ]),
            money_earned_by_grandchild_nodes_last_month=sum([
                a.amount for a in Account.objects.filter(
                    cid=self.id, create_time__gte=last_month_bgn,
                    create_time__lt=last_month_end, source=FROM_GRANDCHILD
                )
            ]),
        )

    @classmethod
    def get_trees(cls):
        #parents = cls.objects.filter(parent_id=None)
        all_nodes = cls.objects.all().order_by('id')
        id_nodes = {}
        for node in all_nodes:
            id_nodes[node.id] = node
        trees = []
        for node in all_nodes:
            if node.parent_id is None:
                new_tree = cls.generate_tree(node, id_nodes)
                trees.append(new_tree)
        return trees

    @classmethod
    def generate_tree(cls, root, id_nodes):

        def _render_branch(parent, id_nodes):
            children_ids = parent['children']
            if not children_ids:
                 return
            parent['children'] = {}
            for child_id in children_ids:
                parent['children'][child_id] = id_nodes.pop(child_id).get_info()
                _render_branch(parent['children'][child_id], id_nodes)

        tree = {-1: root.get_info()}
        root = tree[-1]
        _render_branch(root, id_nodes)
        return tree

    @classmethod
    def get_tree_by_root_id(cls, root_id):
        rnode = cls.get(root_id)
        root_id = rnode.root_id if rnode.root_id else rnode.id
        family_nodes = cls.objects.filter(root_id=root_id)
        id_nodes = {}
        for node in family_nodes:
            id_nodes[node.id] = node
        tree = cls.generate_tree(rnode, id_nodes)
        return tree


