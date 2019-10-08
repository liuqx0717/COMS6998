import datetime
import json
import logging
import math
import os
import time

import dateutil.parser
import phonenumbers


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def validate_order(phoneNumber, diningDate, diningTime):
    if phoneNumber is not None and not phonenumbers.is_valid_number(phonenumbers.parse(phoneNumber, "US")):
        return build_validation_result(False,
                                       'phoneNumber',
                                       'Please provide a valid phone number.')

    if diningDate is not None:
        if not isvalid_date(diningDate):
            return build_validation_result(False, 'diningDate', 'I did not understand that, '
                                                                'what date would you like to go to the restaurant?')
        elif datetime.datetime.strptime(diningDate, '%Y-%m-%d').date() < datetime.date.today():
            return build_validation_result(False, 'diningDate', 'You can go to the restaurant from today onwards.  '
                                                                'What day would you like to go?')

    if diningTime is not None:
        if len(diningTime) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'diningTime', None)

        hour, minute = diningTime.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'diningTime', None)

        # if hour < 10 or hour > 16:
        #     # Outside of business hours
        #     return build_validation_result(False, 'PickupTime', 'Our business hours are from ten a m. to five p m. Can you specify a time during this range?')

    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def dining_info_process(intent_request):
    """
    Performs dialog management and fulfillment for ordering flowers.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """

    location = get_slots(intent_request)["location"]
    cuisine = get_slots(intent_request)["cuisine"]
    numberOfPeople = get_slots(intent_request)["numberOfPeople"]
    phoneNumber = get_slots(intent_request)["phoneNumber"]
    diningDate = get_slots(intent_request)["diningDate"]
    diningTime = get_slots(intent_request)["diningTime"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation_result = validate_order(phoneNumber, diningDate, diningTime)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                               'sessionAttributes'] is not None else {}

        return delegate(output_session_attributes, get_slots(intent_request))

    """
    Call for SNS
    """
    if source == "FulfillmentCodeHook":
        return close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Thanks, you have {} people and the dining time is {} {}. We will recommend {} food '
                                 'at {} for you. The information will be sent to you phone number {}'.format(
                          numberOfPeople, diningTime, diningDate, cuisine, location, phoneNumber)})


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'DiningSuggestionsIntent':
        return dining_info_process(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)


test = {
    "messageVersion": "1.0",
    "invocationSource": "FulfillmentCodeHook",
    "userId": "John",
    "sessionAttributes": {},
    "bot": {
        "name": "DiningBot",
        "alias": "$LATEST",
        "version": "$LATEST"
    },
    "outputDialogMode": "Text",
    "currentIntent": {
        "name": "DiningSuggestionsIntent",
        "slots": {
            "location": "New York",
            "cuisine": "Chinese",
            "numberOfPeople": "6",
            "phoneNumber": "9299907314",
            "diningDate": "2030-11-08",
            "diningTime": "11:00"
        },
        "confirmationStatus": "None"
    }
}

res = lambda_handler(test, {})
print(json.dumps(res, indent=2))
