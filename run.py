from sqlalchemy import Table, Column, String, Integer, Date
from sqlalchemy.orm import mapper
from createsend import *
import inspect
import db
import tables
from datetime import datetime, date

from colorama import init, Fore
init()

CREATESEND_API_KEY = 'INSERT_API_KEY_HERE'
NUM_CUSTOM_FIELDS = 35

# This class is used to map SQL Tables/Views to a Python class.
# More complex API calls will probably need more than one table
class Map(object):
    pass


# This class is used to map SF_CARLYLE_CLIENT_LISTS to a Python class.
class ClientListsMap(object):
    pass


# This class is used to map SF_CARLYLE_SEGMENTS to a Python class.
class SegmentMap(object):
    pass


# This class is used to map SF_CARLYLE_SEGMENT_USERS to a Python class.
class SegmentUsersMap(object):
    pass


# This class is used to map SF_CARLYLE_CLIENT_LISTS to a Python class.
class UsersMap(object):
    pass


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class BadSegmentUserError(Error):
    def __init__(self, segment_user_id, expr, msg):
        self.segment_user_id = segment_user_id
        self.expr = expr
        self.msg = msg

segment_table = tables.get_segment_class()
mapper(SegmentMap, segment_table)

segment_users_table = tables.get_segment_users_class()
mapper(SegmentUsersMap, segment_users_table)

users_table = tables.get_users_class()
mapper(UsersMap, users_table)


def notify_of_exception(error_message):
    print(Fore.RED + '!!! ' + error_message + ' !!!' + Fore.RESET)
    import pdb; pdb.set_trace()


def get_client_info():
    cs = CreateSend({'api_key': CREATESEND_API_KEY})
    clients = cs.clients()
    for client in clients:
        cl = Client(
            {'api_key': CREATESEND_API_KEY},
            client.ClientID)
        details = cl.details()
        for member in inspect.getmembers(details.BasicDetails):
            print member
        break

"""

The final and best method to do this is to use the "Importing many subscribers" function (http://www.campaignmonitor.com/api/subscribers/#importing_subscribers).
This function also updates current subscribers if the email is already in the list. So you can update 1000 subscribers in 1 API call including custom fields.
Thanks to Campaign Monitor support for their help on that.
https://www.campaignmonitor.com/forums/topic/6850/bulk-custom-field-update/

"""

def update_custom_fields():
    """
        According to Campaign Monitor documentations, this:
        Allows you to add many subscribers to a subscriber list in one API request, including custom field data if supplied.
        If a subscriber (email address) already exists, their name and any custom field values are updated with whatever is passed in.

        Since we can assume that all users have already been subscribed through Salesforce, we can update CFs in bulk this way.
        Method signature: import_subscribers(self, list_id, subscribers, resubscribe, queue_subscription_based_autoresponders=False, restart_subscription_based_autoresponders=False)
        https://www.campaignmonitor.com/api/subscribers/#importing_many_subscribers
    """


def get_oracle_segment_ids():
    """ Return all Oracle segment IDs in the database
    :return: list
    """
    ret = []

    # res = session.query(SegmentMap.id).all()
    # for seg in res:
    #     ret.append(seg[0])

    ret = [
        6282,
        # CAS parents 4:55am
        13393,
        # CAPS ------ 4:58am
        6322,
        # GS -------- 5:05am
        6323,
        # Sem ------- 5:09am
        6342,
        # EnrChecklistNew
        13842
    ]

    return ret


def get_unsynced_segment_users_by_segment_id(oracle_segment_id):

    res = session.query(SegmentUsersMap).filter_by(
        segid=oracle_segment_id,
        sync=None
    )
    return res

def get_segment_users_by_segment_id(oracle_segment_id):

    res = session.query(SegmentUsersMap).filter_by(
        segid=oracle_segment_id
    )
    return res


def get_user_by_sf_id(sf_id):

    res = session.query(UsersMap).filter_by(
        sf_id=sf_id
    )

    ret = []

    if res.count() == 1:
        ret = res[0]
    elif res.count() == 0:
        """ No results exception """
    elif res.count() > 1:
        """ Many results exception """

    return ret


def get_oracle_segment_by_id(oracle_segment_id):
    """
    :return: SegmentMap
    """
    ret = []

    res = session.query(SegmentMap).filter_by(id=oracle_segment_id)

    for r in res:
        ret.append(r.id)
    if res.count() == 1:
        ret = res[0]
    elif res.count() == 0:
        """ No results exception """
    elif res.count() > 1:
        """ Many results exception """

    return ret


def get_custom_field_name(seg, title):
    """ Derives the custom field name from the ID and title of the segment in Oracle
    :param seg: A sqlalchemy segment object
    :return: string
    """
    cfname = str(seg.id) + '-' + title
    cfname = cfname.replace('/', '-')
    return cfname


def handle_segment_creation(seg):
    """ If the segment does not yet exist in Carlyle, this method will create it
    :returns: boolean (True if the segment is new), string (Carlyle segment ID)
    """
    # Let's create the segment in the given list
    cdlistid = seg.list_id
    cdlist = List({'api_key': CREATESEND_API_KEY}, list_id=cdlistid)

    if seg.cd_segment_id is not None and not seg.sync_status:
        # We also need to create custom fields specified in Oracle
        # Currently, this script is based on the assumption of 30
        # custom fields, which reflects the schema in Oracle
        cfs = cdlist.custom_fields()
        for i in range(NUM_CUSTOM_FIELDS):
            titlekey = 'cf_' + str(i+1) + '_title'
            typekey = 'cf_' + str(i+1) + '_type'
            cftitle = seg.__getattribute__(titlekey)
            if cftitle:
                cftitle = get_custom_field_name(seg, cftitle)

            # Here we iterate through all the custom fields that already exist
            # in Carlyle. If a CF already exists, we skip to the next one
            for cf in cfs:
                if cf.FieldName == cftitle:
                    print(Fore.GREEN + cftitle + ' Exists' + Fore.RESET)
                    existingcf = True
                    break
                else:
                    existingcf = False
            if existingcf:
                continue

            cftype = seg.__getattribute__(typekey)
            if cftitle and cftype:
                cdlist.create_custom_field(cftitle, cftype)
            else:
                # If either the title or type are not available, we're done creating CFs
                break
        seg.sync_status = 'Success'
        seg.sync_date = date.today()
        session.add(seg)
        session.commit()
        return False, seg.cd_segment_id
    if seg.cd_segment_id is not None:
        return False, seg.cd_segment_id
    else:
        # The rulegroup simply contains the ID of the segment
        cfname = get_custom_field_name(seg, seg.title)

        # First we need to create a custom field on the list to contain the membership
        cdlist.create_custom_field(cfname, "Number")

        # Now create the rest of the custom fields
        for i in range(NUM_CUSTOM_FIELDS):
            titlekey = 'cf_' + str(i+1) + '_title'
            typekey = 'cf_' + str(i+1) + '_type'
            cftitle = seg.__getattribute__(titlekey)
            if cftitle:
                cftitle = get_custom_field_name(seg, cftitle)

            cftype = seg.__getattribute__(typekey)
            if cftitle and cftype:
                cdlist.create_custom_field(cftitle, cftype)
            else:
                # If either the title or type are not available, we're done creating CFs
                break

        # After the custom fields have been created successfully, we can create the rule
        rulegroups = [{"Rules": [{"RuleType": cfname, "Clause": "EQUALS 1"}]}]
        cdseg = Segment({'api_key': CREATESEND_API_KEY})
        cdseg_id = cdseg.create(cdlistid, str(seg.id) + ' ' + seg.title, rulegroups)
        seg.cd_segment_id = cdseg_id
        seg.sync_status = 'Success'
        seg.sync_date = date.today()
        session.add(seg)
        session.commit()
        return True, cdseg_id


def segment_user_custom_fields(seg, segment_user):
    custom_fields = []
    try:
        for i in range(NUM_CUSTOM_FIELDS):
            cfkey = 'cf_' + str(i+1)
            cftitle = 'cf_' + str(i+1) + '_title'
            cftype = 'cf_' + str(i+1) + '_type'
            cfvalue = segment_user.__getattribute__(cfkey)
            cftitle = seg.__getattribute__(cftitle)
            cftype = seg.__getattribute__(cftype)
            # Passing 'Clear': False means that we do not want to remove any existing value
            cfclear = False
            if cftitle and cftype:
                cfname = get_custom_field_name(seg, cftitle)
                if not cfvalue:
                    cfvalue = ''
                    # Passing 'Clear': True means that we want to remove any existing value
                    cfclear = True
                elif cftype == "Date":
                    if not cfvalue.isdigit():
                        raise BadSegmentUserError(segment_user.id, cfvalue, "Illegal characters")
                    elif cftype == "Date" and len(cfvalue) != 8:
                        raise BadSegmentUserError(segment_user.id, cfvalue, "Length mismatch")
                    elif cftype == "Date":
                        # Dates are stored in Oracle as yyyymmdd, we want yyyy/mm/dd
                        cfvalue = cfvalue[0:4] + '/' + cfvalue[4:6] + '/' + cfvalue[6:8]

                cf = {'Clear': cfclear, 'Value': cfvalue, 'Key': cfname}
                custom_fields.append(cf)
            elif (cftype and not cftitle) or (cftitle and not cftype):
                # There's no field by that name, so we're done
                break
    except BadSegmentUserError as e:
        notify_of_exception(
            str(e.msg) + ' in ' +
            str(e.expr) + '(Oracle ID: ' +
            str(e.segment_user_id) + ')'
        )
        return False

    return custom_fields


def populate_segment_users(oracle_segment_id):
    batch_import_users(oracle_segment_id)
    print(Fore.RED + 'First sync of users in ' + str(oracle_segment_id) + Fore.RESET)


def update_segment_users(oracle_segment_id):

    batch_import_users(oracle_segment_id)
    #
    # TODO: TRYING TO MASS UPDATE SYNC STATUS HERE
    # FOR SOME REASON IT'S NOT WORKING, EVEN WHEN
    # I GIVE THE SESSION DIRECTLY
    #
    # updt = segment_users.update({'sync_status': 'Success'})
    #
    # session.commit()
    print(Fore.RED + 'Updated users in ' + str(oracle_segment_id) + Fore.RESET)


def batch_import_users(oracle_segment_id):
    seg = get_oracle_segment_by_id(oracle_segment_id)
    list_id = seg.list_id

    segment_users = get_unsynced_segment_users_by_segment_id(oracle_segment_id)

    subscriber = Subscriber({'api_key': CREATESEND_API_KEY})
    import_list = []
    batch_results = []
    # batch subscribers into lots of < 1000
    batch_limit = 0
    total_elements = 0
    batch_num = 0
    for segment_user in segment_users:
        batch_limit += 1

        user = get_user_by_sf_id(segment_user.sf_id)
        import_user = {
            'EmailAddress': user.email,
            'Name': user.first_name + ' ' + user.last_name
        }

        custom_fields = segment_user_custom_fields(seg, segment_user)

        if custom_fields:
            import_user['CustomFields'] = custom_fields
        else:
            continue
        # We also add the values for VanityList and VanityRole
        if segment_user.list:
            vanity_list = {'Clear': False, 'Value': segment_user.list, 'Key': 'Vanity List'}
        else:
            vanity_list = {'Clear': True, 'Value': '', 'Key': 'Vanity List'}

        import_user['CustomFields'].append(vanity_list)

        if segment_user.role:
            vanity_role = {'Clear': False, 'Value': segment_user.role, 'Key': 'Vanity Role'}
        else:
            vanity_role = {'Clear': True, 'Value': '', 'Key': 'Vanity Role'}

        import_user['CustomFields'].append(vanity_role)
        # Finally, we add a value to the custom field used for the segment rule
        cfname = get_custom_field_name(seg, seg.title)
        segcf = {'Clear': False, 'Value': '1', 'Key': cfname}
        import_user['CustomFields'].append(segcf)
        import_list.append(import_user)
        # We send our subscribers either at just under 1000 or the final batch
        if batch_limit == 999 or (batch_limit + total_elements) == segment_users.count():
            total_elements += 999
            batch_num += 1
            filename = "import_%s.txt" % date.today().isoformat()
            logfile = open(filename, "a")
            logfile.write("\n========\nBatch %s\n========\n" % batch_num)
            # Createsend limits us to 1000 users, so we need to send this batch
            # we'll try to send the data 3 times,
            for x in range(3):
                try:
                    import_result = subscriber.import_subscribers(list_id, import_list, False)
                    logfile.write("Failure Details:\n")
                    for detail in import_result.FailureDetails:
                        logfile.write("\tEmail: %s, Code: %s, Message: %s\n" % (detail.EmailAddress, detail.Code, detail.Message))
                    logfile.write("Total Unique Emails Submitted: %s\n" % import_result.TotalUniqueEmailsSubmitted)
                    logfile.write("Total Existing Subscribers: %s\n" % import_result.TotalExistingSubscribers)
                    logfile.write("Total New Subscribers: %s\n" % import_result.TotalNewSubscribers)
                    logfile.write("Duplicate Emails in Submission: %s\n" % import_result.DuplicateEmailsInSubmission)
                    logfile.close()
                    print (Fore.GREEN + "Batch " + str(batch_num) + " Complete" + Fore.RESET)
                    batch_results.append(import_result)

                    # Reset our counter and clear out the import list
                    import_list = []
                    batch_limit = 0
                    break
                except ServerError:
                    print (Fore.RED + "Server Error " + str(x) + Fore.RESET)
                    logfile.write("Server Error %s" % x)

    segment_users.update({'sync': 'Success'})
    session.commit()


def handle_segment_expiration(seg):

    """

    :param seg:
    :return: boolean, boolean (attempted expiration, expiration succeeded)
    """
    present = date.today()
    print (Fore.GREEN + "Segment Expiration: " + str(seg.expires) + Fore.RESET)
    if seg.expires is None or seg.expires >= present:
        return False, False
    else:
        cdlist = List({'api_key': CREATESEND_API_KEY}, list_id=seg.list_id)
        cdseg = Segment({'api_key': CREATESEND_API_KEY}, segment_id=seg.cd_segment_id)

        filename = "expiration_%s.txt" % date.today().isoformat()
        expiration_log = open(filename, "a")
        expiration_log.write("\n===============\nExpiration %s\n===============\n" % seg.id)

        try:
            cdseg.delete()
            delete_segment_custom_fields(cdlist, seg.id, expiration_log)
        except BadRequest, e:
            expiration_log.write("Segment deletion failed with %s: %s\n" % (e.data.Code, e.data.Message))
            print(Fore.RED + "Segment deletion for %s failed with %s: %s" % (seg.id, e.data.Code, e.data.Message) + Fore.RESET)
            return True, False

        seg.sync_status = 'Expired'
        session.add(seg)
        session.commit()
        return True, True


def delete_segment_custom_fields(cdlist, segid, expiration_log):
    cfs = cdlist.custom_fields()
    cf_keys_to_delete = []
    for cf in cfs:
        cf_key = cf.Key
        # Keys are always wrapped in square brackets
        # Segment keys contain the Oracle segment ID first, followed by a dash
        cf_segid = cf_key.strip('[]').split('-')[0]
        try:
            if int(cf_segid) == segid:
                cf_keys_to_delete.append(cf_key)
        except ValueError:
            continue

    for cf_key in cf_keys_to_delete:
        try:
            cdlist.delete_custom_field(cf_key)
            expiration_log.write("Deleted CF: %s\n" % cf_key)
        except BadRequest, e:
            expiration_log.write("Custom field deletion failed with %s: %s\n" % (e.data.Code, e.data.Message))
            print(Fore.RED + "Custom field deletion for %s failed failed with %s: %s" % (segid, e.data.Code, e.data.Message) + Fore.RESET)
        except ServerError:
            expiration_log.write("500 Error")

# def create_cd_segment():
#
#
# def update_segment(seg_id):
    # Should update_segment = delete_segment + create_segment?

# Iterate through segments
# MAIN LOOP
engine, metadata, session = db.get_connection()
for oid in get_oracle_segment_ids():
    segment = get_oracle_segment_by_id(oid)
    attempted, expired = handle_segment_expiration(segment)
    if attempted:
        if expired:
            print(Fore.YELLOW + 'Segment expired with id ' + str(segment.id) + Fore.RESET)
            # Segment expired, go next
            # TODO: delete the segment
            # do we need to individually delete segment users? i don't think so
        else:
            print(Fore.RED + 'Segment expiration failed for id ' + str(segment.id) + Fore.RESET)
        continue
    created, segmentid = handle_segment_creation(segment)
    if created:
        print(Fore.GREEN + 'Segment Created with id ' + segmentid + Fore.RESET)
        # TODO: write initial population logic
        # the only difference between pop and update is that
        # we won't check segment user sync status on population
        populate_segment_users(segment.id)
    else:
        print(Fore.GREEN + 'Segment Updated with id ' + segmentid + Fore.RESET)
        update_segment_users(segment.id)
