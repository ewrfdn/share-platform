from math import ceil
from peewee import Query

def paginate_query(query: Query, page: int = 1, page_size: int = 10):
    """
    对 Peewee 查询进行分页处理
    
    Args:
        query: Peewee Query 对象
        page: 当前页码 (从1开始)
        page_size: 每页数量
        
    Returns:
        dict: {
            'items': list of items for current page,
            'total': total number of items,
            'page': current page number,
            'page_size': number of items per page,
            'total_pages': total number of pages,
            'has_next': whether there is a next page,
            'has_prev': whether there is a previous page
        }
    """
    # 确保页码和每页数量为正整数
    page = max(1, page)
    page_size = max(1, page_size)
    
    # 计算总记录数
    total = query.count()
    
    # 计算总页数
    total_pages = ceil(total / page_size)
    
    # 确保页码不超过总页数
    page = min(page, total_pages) if total_pages > 0 else 1
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 获取当前页的数据
    items = [item.to_json() for item in query.offset(offset).limit(page_size)]
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    } 