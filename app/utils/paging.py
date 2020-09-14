
def get_paging(items, page, limit=10):
    page = int(page)
    limit = int(limit)
    pages = len(items) // limit

    if page - 1 > pages or page <= 0:
        return [], 0
    start = (page - 1) * limit
    end = start + limit if start + limit < len(items) else len(items)
    res = []
    for i in range(start, end):
        res.append(items[i])
    return res, len(items)