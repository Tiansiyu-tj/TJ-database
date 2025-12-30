from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from typing import Optional
from ..database import engine_metro, get_db_metro
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/stations')
def stations(limit: int = 1000):
    """返回站点列表"""
    with engine_metro.connect() as conn:
        rows = conn.execute(text('SELECT `stationID` AS `id`, `name`, `lon`, `lat` FROM `station` ORDER BY `stationID` LIMIT :limit'), {'limit': limit}).fetchall()
        data = [dict(r._mapping) for r in rows]
    return {'code': 0, 'message': '', 'data': data}


@router.get('/timesegments')
def timesegments(recordDate: Optional[str] = Query(None), limit: int = 1000):
    """返回时间段表（可按 recordDate 过滤，或按 limit 限制条数）
    注意：当直接在 Python 中调用此函数（非通过 HTTP）时，recordDate 的默认值可能是 FastAPI 的 Query 对象，
    因此在使用前需要做类型校验和转换以避免将 Query 对象传给 SQL。"""
    # 当通过脚本直接调用时，recordDate 可能是 Query(None)；仅在其为字符串时才使用
    rd = recordDate if isinstance(recordDate, str) else None

    q = 'SELECT `Slot`, `recordDate`, `StartTime`, `EndTime` FROM `timesegment`'
    params = {}
    if rd:
        q += ' WHERE `recordDate` = :recordDate'
        params['recordDate'] = rd
    q += ' ORDER BY `Slot` LIMIT :limit'
    params['limit'] = limit

    with engine_metro.connect() as conn:
        rows = conn.execute(text(q), params).fetchall()
        data = [dict(r._mapping) for r in rows]
    return {'code': 0, 'message': '', 'data': data}


@router.get('/inflow')
def inflow(Slot: Optional[int] = Query(None), stationID: Optional[int] = Query(None), limit: int = 1000):
    """返回 inflow 表的原始行，支持按 Slot / stationID 过滤"""
    q = 'SELECT * FROM `inflow`'
    params = {}
    conds = []
    if Slot is not None:
        conds.append('`Slot` = :Slot')
        params['Slot'] = Slot
    if stationID is not None:
        conds.append('`stationID` = :stationID')
        params['stationID'] = stationID
    if conds:
        q += ' WHERE ' + ' AND '.join(conds)
    q += ' LIMIT :limit'
    params['limit'] = limit
    with engine_metro.connect() as conn:
        rows = conn.execute(text(q), params).fetchall()
        data = [dict(r._mapping) for r in rows]
    return {'code': 0, 'message': '', 'data': data}


@router.get('/outflow')
def outflow(Slot: Optional[int] = Query(None), stationID: Optional[int] = Query(None), limit: int = 1000):
    q = 'SELECT * FROM `outflow`'
    params = {}
    conds = []
    if Slot is not None:
        conds.append('`Slot` = :Slot')
        params['Slot'] = Slot
    if stationID is not None:
        conds.append('`stationID` = :stationID')
        params['stationID'] = stationID
    if conds:
        q += ' WHERE ' + ' AND '.join(conds)
    q += ' LIMIT :limit'
    params['limit'] = limit
    with engine_metro.connect() as conn:
        rows = conn.execute(text(q), params).fetchall()
        data = [dict(r._mapping) for r in rows]
    return {'code': 0, 'message': '', 'data': data}


@router.get('/weather')
def weather(recordDate: Optional[str] = Query(None), limit: int = 100):
    """返回天气记录，支持按 recordDate 过滤（若 recordDate 为 None 则返回最新若干条）"""
    rd = recordDate if isinstance(recordDate, str) else None
    q = 'SELECT * FROM `weather`'
    params = {}
    if rd:
        q += ' WHERE `recordDate` = :recordDate'
        params['recordDate'] = rd
    q += ' ORDER BY `recordDate` DESC, `recordTime` DESC LIMIT :limit'
    params['limit'] = limit
    with engine_metro.connect() as conn:
        rows = conn.execute(text(q), params).fetchall()
        data = [dict(r._mapping) for r in rows]
    return {'code': 0, 'message': '', 'data': data}


@router.get('/top-od')
def top_od(recordDate: str = "2017-06-10", limit: int = 10):
    """返回指定日期的热门OD流量（按总流量排序）"""
    with engine_metro.connect() as conn:
        # 使用提供的SQL逻辑查询
        query = """
        SELECT
            o.O_Station,
            o.D_Station,
            SUM(o.Tot_F) AS Tot_F
        FROM ODFlow o
        JOIN (
            -- 先查询 2017-06-10 当天所有 Slot，提高性能
            SELECT Slot
            FROM TimeSegment
            WHERE recordDate = :recordDate
        ) t ON o.Slot = t.Slot
        GROUP BY o.O_Station, o.D_Station
        ORDER BY Tot_F DESC
        LIMIT :limit
        """
        params = {"recordDate": recordDate, "limit": limit}
        rows = conn.execute(text(query), params).fetchall()
        data = [dict(r._mapping) for r in rows]
    return {'code': 0, 'message': '', 'data': data}
