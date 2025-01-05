def calculate_offsets(offset: int, limit: int, total: int):
    next_offset = (int(offset or 0) + int(limit or 0)) if (int(offset or 0) + int(limit or 0)) < int(total) else 0
    previous_offset = (int(offset or 0) - int(limit or 0)) if (int(offset or 0) - int(limit or 0)) >= 0 else 0
    return next_offset, previous_offset