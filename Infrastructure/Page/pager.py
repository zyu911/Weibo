#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Pagentation:
    def __init__(self, current_page, all_item, base_url):
        try:
            page = int(current_page)
        except:
            page = 1
        if page < 1:
            page = 1

        all_pager, c = divmod(all_item, 5)
        if c > 0:
            all_pager += 1

        self.current_page = page
        self.all_pager = all_pager
        self.base_url = base_url

    @property
    def start(self):
        return (self.current_page - 1) * 5

    @property
    def end(self):
        return self.current_page * 5

    def string_pager(self):
        list_page = []

        if self.all_pager < 11:
            s = 1
            t = self.all_pager + 1
        else:
            if self.current_page < 6:
                s = 1
                t = 12
            else:
                if (self.current_page + 5) < self.all_pager:
                    s = self.current_page - 5
                    t = self.current_page + 5 + 1
                else:
                    s = self.all_pager - 11
                    t = self.all_pager + 1

        if self.current_page == 1:
            prev = '<a class="left-divmod" href="javascript:void(0)">上一页</a>'
        else:
            prev = '<a class="left-divmod" href="/index/%s">上一页</a>' % (self.current_page - 1)
        list_page.append(prev)

        for p in range(s, t):
            if p == self.current_page:
                temp = '<a class="left-divmod" style="background-color: #b2dba1" href="/index/%s">%s</a>' % (p, p)
            else:
                temp = '<a class="left-divmod" href="/index/%s">%s</a>' % (p, p)
            list_page.append(temp)

        if self.current_page == self.all_pager:
            temp = '<a class="left-divmod" href="javascript:void(0)">下一页</a>'
        else:
            temp = '<a class="left-divmod" href="/index/%s">下一页</a>' % (self.current_page + 1)
        list_page.append(temp)

        str_page = "".join(list_page)
        return str_page
