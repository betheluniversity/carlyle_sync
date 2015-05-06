from sqlalchemy import Table, Column, String, Integer, Date, Index
import db

def get_client_lists_class():
    engine, metadata, session = db.get_connection()
    client_lists_table = Table('SF_CARLYLE_CLIENT_LISTS', metadata,
                               Column('client_id', String(64), nullable=False),
                               Column('list_id', String(256), nullable=False),
                               Column('list_name', String(256), nullable=True)
    )

    return client_lists_table


def get_users_class():
    engine, metadata, session = db.get_connection()
    users_table = Table('SF_CARLYLE_USERS', metadata,
                        Column('first_name', String(64), nullable=True),
                        Column('last_name', String(64), nullable=True),
                        Column('sf_id', String(18), nullable=False, primary_key=True),
                        Column('email', String(256), nullable=True)
    )

    return users_table

def get_segment_users_class():
    engine, metadata, session = db.get_connection()
    segment_users_table = Table('SF_CARLYLE_SEGMENT_USERS', metadata,
                                Column('segid', Integer, nullable=False),
                                Column('sf_id', String(18), nullable=False),
                                Column('cf_1', String(250), nullable=True),
                                Column('cf_2', String(250), nullable=True),
                                Column('cf_3', String(250), nullable=True),
                                Column('cf_4', String(250), nullable=True),
                                Column('cf_5', String(250), nullable=True),
                                Column('cf_6', String(250), nullable=True),
                                Column('cf_7', String(250), nullable=True),
                                Column('cf_8', String(250), nullable=True),
                                Column('cf_9', String(250), nullable=True),
                                Column('cf_10', String(250), nullable=True),
                                Column('cf_11', String(250), nullable=True),
                                Column('cf_12', String(250), nullable=True),
                                Column('cf_13', String(250), nullable=True),
                                Column('cf_14', String(250), nullable=True),
                                Column('cf_15', String(250), nullable=True),
                                Column('cf_16', String(250), nullable=True),
                                Column('cf_17', String(250), nullable=True),
                                Column('cf_18', String(250), nullable=True),
                                Column('cf_19', String(250), nullable=True),
                                Column('cf_20', String(250), nullable=True),
                                Column('cf_21', String(250), nullable=True),
                                Column('cf_22', String(250), nullable=True),
                                Column('cf_23', String(250), nullable=True),
                                Column('cf_24', String(250), nullable=True),
                                Column('cf_25', String(250), nullable=True),
                                Column('cf_26', String(250), nullable=True),
                                Column('cf_27', String(250), nullable=True),
                                Column('cf_28', String(250), nullable=True),
                                Column('cf_29', String(250), nullable=True),
                                Column('cf_30', String(250), nullable=True),
                                Column('cf_31', String(250), nullable=True),
                                Column('cf_32', String(250), nullable=True),
                                Column('cf_33', String(250), nullable=True),
                                Column('cf_34', String(250), nullable=True),
                                Column('cf_35', String(250), nullable=True),
                                Column('list', String(250), nullable=True),
                                Column('role', String(250), nullable=True),
                                Column('sync', String(20), nullable=True),
                                Column('id', Integer, nullable=False, primary_key=True)
    )
    # Index('SYS_C00383283', segment_users_table.c.sf_carlyle_segment_id, segment_users_table.c.sf_id)
    return segment_users_table


def get_segment_class():
    engine, metadata, session = db.get_connection()
    segment_table = Table('SF_CARLYLE_SEGMENT', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('sync_status', String(1024), nullable=True),
                          Column('sync_date', Date),
                          Column('cd_segment_id', String(length=256), nullable=True),
                          Column('list_id', String(length=256), nullable=False),
                          Column('title', String(20), nullable=True),
                          Column('activity', Date),
                          Column('expires', Date),
                          Column('user_id', String(8), nullable=True),
                          Column('description', String(100), nullable=True),
                          Column('cf_1_title', String(250), nullable=True),
                          Column('cf_2_title', String(250), nullable=True),
                          Column('cf_3_title', String(250), nullable=True),
                          Column('cf_4_title', String(250), nullable=True),
                          Column('cf_5_title', String(250), nullable=True),
                          Column('cf_6_title', String(250), nullable=True),
                          Column('cf_7_title', String(250), nullable=True),
                          Column('cf_8_title', String(250), nullable=True),
                          Column('cf_9_title', String(250), nullable=True),
                          Column('cf_10_title', String(250), nullable=True),
                          Column('cf_11_title', String(250), nullable=True),
                          Column('cf_12_title', String(250), nullable=True),
                          Column('cf_13_title', String(250), nullable=True),
                          Column('cf_14_title', String(250), nullable=True),
                          Column('cf_15_title', String(250), nullable=True),
                          Column('cf_16_title', String(250), nullable=True),
                          Column('cf_17_title', String(250), nullable=True),
                          Column('cf_18_title', String(250), nullable=True),
                          Column('cf_19_title', String(250), nullable=True),
                          Column('cf_20_title', String(250), nullable=True),
                          Column('cf_21_title', String(250), nullable=True),
                          Column('cf_22_title', String(250), nullable=True),
                          Column('cf_23_title', String(250), nullable=True),
                          Column('cf_24_title', String(250), nullable=True),
                          Column('cf_25_title', String(250), nullable=True),
                          Column('cf_26_title', String(250), nullable=True),
                          Column('cf_27_title', String(250), nullable=True),
                          Column('cf_28_title', String(250), nullable=True),
                          Column('cf_29_title', String(250), nullable=True),
                          Column('cf_30_title', String(250), nullable=True),
                          Column('cf_31_title', String(250), nullable=True),
                          Column('cf_32_title', String(250), nullable=True),
                          Column('cf_33_title', String(250), nullable=True),
                          Column('cf_34_title', String(250), nullable=True),
                          Column('cf_35_title', String(250), nullable=True),
                          Column('cf_1_type', String(20), nullable=True),
                          Column('cf_2_type', String(20), nullable=True),
                          Column('cf_3_type', String(20), nullable=True),
                          Column('cf_4_type', String(20), nullable=True),
                          Column('cf_5_type', String(20), nullable=True),
                          Column('cf_6_type', String(20), nullable=True),
                          Column('cf_7_type', String(20), nullable=True),
                          Column('cf_8_type', String(20), nullable=True),
                          Column('cf_9_type', String(20), nullable=True),
                          Column('cf_10_type', String(20), nullable=True),
                          Column('cf_11_type', String(20), nullable=True),
                          Column('cf_12_type', String(20), nullable=True),
                          Column('cf_13_type', String(20), nullable=True),
                          Column('cf_14_type', String(20), nullable=True),
                          Column('cf_15_type', String(20), nullable=True),
                          Column('cf_16_type', String(20), nullable=True),
                          Column('cf_17_type', String(20), nullable=True),
                          Column('cf_18_type', String(20), nullable=True),
                          Column('cf_19_type', String(20), nullable=True),
                          Column('cf_20_type', String(20), nullable=True),
                          Column('cf_21_type', String(20), nullable=True),
                          Column('cf_22_type', String(20), nullable=True),
                          Column('cf_23_type', String(20), nullable=True),
                          Column('cf_24_type', String(20), nullable=True),
                          Column('cf_25_type', String(20), nullable=True),
                          Column('cf_26_type', String(20), nullable=True),
                          Column('cf_27_type', String(20), nullable=True),
                          Column('cf_28_type', String(20), nullable=True),
                          Column('cf_29_type', String(20), nullable=True),
                          Column('cf_30_type', String(20), nullable=True),
                          Column('cf_31_type', String(20), nullable=True),
                          Column('cf_32_type', String(20), nullable=True),
                          Column('cf_33_type', String(20), nullable=True),
                          Column('cf_34_type', String(20), nullable=True),
                          Column('cf_35_type', String(20), nullable=True)
    )

    return segment_table