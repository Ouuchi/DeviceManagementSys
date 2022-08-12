from django.utils.safestring import mark_safe

class Pageination(object):
    def __init__(self,request,queryset,page_size=10,page_param="page",plus=5):
        import copy
        query_dict=copy.deepcopy(request.GET)
        query_dict._mutable=True
        self.query_dict=query_dict
        self.page_param=page_param



        page=request.GET.get(page_param,"1")
        if page.isdecimal():
            page=int(page)
        else:
            page=1
        self.page=page
        self.page_size=page_size
        self.start=(page-1)*page_size
        self.end=page*page_size
        self.page_queryset=queryset[self.start:self.end]
        ### 页码
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count = total_page_count + 1
        self.plus=plus


        self.total_page_count=total_page_count


    def html(self):

        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            ## 数据库中的数据比较多 >11页

            ## 当前页<5时
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) >= self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []
        self.query_dict.setlist(self.page_param,[1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            pre = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            pre = '<li ><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(pre)

        ## 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)

            page_str_list.append(ele)

        ## 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page+1])
            nex = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nex = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(nex)

        page_string = mark_safe("".join(page_str_list))
        return page_string













