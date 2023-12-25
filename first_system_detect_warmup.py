# The code is about simulating a call center, with two kinds of customers and three kind of lines.
# MohammadMahdi Ghasemloo, Mohammad erfan Naderloo
# Last edit: 11 pm 8/5/2022

import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl

def Exponential(lambd):
    r = random.random()
    return -(1 / lambd) * math.log(r)


def Uniform(a, b):
    r = random.random()
    return a + (b - a) * r

# if you are not about to have so many replications and preferably one replication, uncomment the code below to have information printed.
def print_header():
    print('Event Type'.ljust(15) + '\t' + 'Event Time'.ljust(15) + '\t' +
          'Special Customer Queue Length'.ljust(15) + '\t' + 'Normal Customer Queue Length'.ljust(
        15) + '\t'   + 'Technical Special Customer Queue Length'.ljust(
        15) + '\t' + 'Technical Normal Customer Queue Length'.ljust(15) + '\t' + 'Specialist Server Status'.ljust(
        15) + '\t' + 'Beginner Server Status'.ljust(15) + 'Technical Server Status'.ljust(15))

    print('----------------------------------------------------------------------------------')


# for printing the table
def nice_print(current_state, current_event):
    print(str(current_event['Event Type']).ljust(15) + '\t' + str(round(current_event['Event Time'], 4)).ljust(
        15) + '\t' + str(current_state['Special Customer Queue Length']).ljust(15) + '\t' + str(
        current_state['Normal Customer Queue Length']).ljust(15)  + '\t' + str(
        current_state['Technical Special Customer Queue Length']).ljust(15) + '\t' + str(
        current_state['Technical Normal Customer Queue Length']).ljust(15) + '\t' + str(
        current_state['Specialist Server Status']).ljust(15) + '\t' + str(
        current_state['Beginner Server Status']).ljust(15) + '\t' + str(current_state['Technical Server Status']).ljust(
        15))


# to store data from replications we define lists here.
customer_churn_total = list()

special_service_starters_total = list()
max_special_customer_queue_length_total = list()
max_normal_customer_queue_length_total = list()
max_special_customer_again_call_queue_length_total = list()
max_normal_customer_again_call_queue_length_total = list()
max_special_customer_technical_queue_length_total = list()
max_normal_customer_technical_queue_length_total = list()
mean_special_customer_queue_length_total = list()
mean_normal_customer_queue_length_total = list()
mean_special_customer_again_call_queue_length_total = list()
mean_normal_customer_again_call_queue_length_total = list()
mean_special_customer_technical_queue_length_total = list()
mean_normal_customer_technical_queue_length_total = list()

max_special_customer_queue_waiting_time_total = list()
max_normal_customer_queue_length_waiting_time_total = list()
max_special_customer_again_call_queue_waiting_time_total = list()
max_normal_customer_again_call_queue_waiting_time_total = list()
max_special_customer_technical_queue_waiting_time_total = list()
max_normal_customer_technical_queue_waiting_time_total = list()
mean_special_customer_queue_waiting_time_total = list()
mean_normal_customer_queue_waiting_time_total = list()

mean_special_customer_again_call_queue_waiting_time_total = list()
mean_normal_customer_again_call_queue_waiting_time_total = list()
mean_special_customer_technical_queue_waiting_time_total = list()
mean_normal_customer_technical_queue_waiting_time_total = list()
mean_special_customer_waiting_time_in_system_total = list()
specialist_servers_utilization_total = list()
beginner_servers_utilization_total = list()
technical_servers_utilization_total = list()

# starting state function, does sum initial work like definig variables and also initializes our variables.
def starting_state():

    # State variables
    state = dict()
    state['Special Customer Queue Length'] = 0 # To store length of special customers in the very first queue
    state['Normal Customer Queue Length'] = 0 # To store length of normal customers in the very first queue
    state['Technical Special Customer Queue Length'] = 0 # To store length of special customers in technical queue
    state['Technical Normal Customer Queue Length'] = 0 # To store length of normal customers in technical queue
    state['Specialist Server Status'] = 0  # 0: Free, 1:one Busy, 2: two busy
    state['Beginner Server Status'] = 0 # 0: Free, 1:one Busy, 2: two busy, 3: three busy
    state['Technical Server Status'] = 0 # 0: Free, 1:one Busy, 2: two busy

    # Data: will save everything
    data = dict()
    data['Special Customers'] = dict()  # To track each special customer, saving their arrival time, time service begins, etc.
    data['Normal Customers'] = dict() # To track each normal customer, saving their arrival time, time service begins, etc.
    data['Last Time Special Customer Queue Length Changed'] = 0
    data['Last Time Normal Customer Queue Length Changed'] = 0
    data['Last Time Technical Special Customer Queue Length Changed'] = 0
    data['Last Time Technical Normal Customer Queue Length Changed'] = 0
    # To check which customer has first arrived, we store them in a dictionary and for each line in a distinct dictionary
    data['Special Queue Customers'] = dict()
    data['Normal Queue Customers'] = dict()
    data['Technical Special Queue Customers'] = dict()
    data['Technical Normal Queue Customers'] = dict()

    # Cumulative Stats
    data['Cumulative Stats'] = dict()
    # Stores busy time in order to calculate utilization
    data['Cumulative Stats']['Specialist Servers Busy Time'] = 0
    data['Cumulative Stats']['Beginner Servers Busy Time'] = 0
    data['Cumulative Stats']['Technical Servers Busy Time'] = 0
    # Stores waiting times, each line and each customer distinctly
    data['Cumulative Stats']['Special Queue Waiting Time'] = 0
    data['Cumulative Stats']['Normal Queue Waiting Time'] = 0
    data['Cumulative Stats']['Technical Special Queue Waiting Time'] = 0
    data['Cumulative Stats']['Technical Normal Queue Waiting Time'] = 0
    # Stores area under queue length, each line and each customer distinctly
    data['Cumulative Stats']['Area Under Special Queue Length Curve'] = 0
    data['Cumulative Stats']['Area Under Normal Queue Length Curve'] = 0
    data['Cumulative Stats']['Area Under Technical Special Queue Length Curve'] = 0
    data['Cumulative Stats']['Area Under Technical Normal Queue Length Curve'] = 0
    # stores immediate service tarters in each line. At the end we implement union on these sets to get general srvice starters.
    data['Special Service Starters'] = set()
    data['Special Service Starters Technical'] = set()
    # Stores customers who left the system and probably left us.
    data['Cumulative Stats']['Customer Churn'] = 0
    # Stores maximums legnths, each line and each kind distinctly
    data['Cumulative Stats']['Max Special Customer Queue Length'] = 0
    data['Cumulative Stats']['Max Normal Customer Queue Length'] = 0
    data['Cumulative Stats']['Max Technical Special Customer Queue Length'] = 0
    data['Cumulative Stats']['Max Technical Normal Customer Queue Length'] = 0
    data['Cumulative Stats']['Max Technical Normal Customer Queue Length'] = 0
    # Stores customers of each line and each kind distinctly
    data['Special Queue Customers All'] = set()
    data['Normal Queue Customers All'] = set()
    data['Technical Special Queue Customers All'] = set()
    data['Technical Normal Queue Customers All'] = set()
    data['Special Customers Waiting Time In System'] = 0

    # Stores maximums waiting times, each line and each kind distinctly
    data['Cumulative Stats']['Max Special Customer Queue Waiting Time'] = 0
    data['Cumulative Stats']['Max Normal Customer Queue Waiting Time'] = 0
    data['Cumulative Stats']['Max Technical Special Customer Queue Waiting Time'] = 0
    data['Cumulative Stats']['Max Technical Normal Customer Queue Waiting Time'] = 0


    # Starting FEL
    future_event_list = list()
    if Uniform(0, 1) > 0.7:
        future_event_list.append(
            {'Event Type': 'Customer Call', 'Event Time': 0, 'Special Customer': 'S1', 'Normal Customer': 'C0',
             'Last Customer': 'S'})
    else:
        future_event_list.append(
            {'Event Type': 'Customer Call', 'Event Time': 0, 'Special Customer': 'S0', 'Normal Customer': 'C1',
             'Last Customer': 'C'})

    return state, future_event_list, data,

# we use this function to make our events with theirs specific features.
def fel_maker(future_event_list, event_type, state, data, clock, customer_special=None,
              customer_normal=None,
              last_customer=None):
    event_time = 0

    if event_type == 'Customer Call':
        if clock % 1440 < 8 * 60:
            shift = 1
        elif clock % 1440 < 16 * 60:
            shift = 2
        else:
            shift = 3

        if shift == 1:
            event_time = clock + Exponential(1 / 1.1)
        elif shift == 2:
            event_time = clock + Exponential(1 / 1.1)
        else:
            event_time = clock + Exponential(1 / 1.1)
    elif event_type == 'Departure From Expert':
        event_time = clock + Exponential(1 / 3)
    elif event_type == 'Departure From Beginner':
        event_time = clock + Exponential(1 / 7)
    elif event_type == 'Departure From Technical':
        event_time = clock + Exponential(0.1)
    elif event_type == 'Leaving Of Tired':
        max_queue_length = state['Special Customer Queue Length'] - 1
        event_time = clock + Uniform(max_queue_length, 25)

    # According to the information given, future event will be made above and will be added to fel as follows.
    new_event = {'Event Type': event_type, 'Event Time': event_time, 'Special Customer': customer_special,
                 'Normal Customer': customer_normal, 'Last Customer': last_customer}
    future_event_list.append(new_event)


def Customer_Call(future_event_list, state, clock, data, customer_special=None, customer_normal=None,
                  last_customer=None):
    # we make the next arrival here.
    if Uniform(0, 1) > 0.6:
        next_customer = 'S' + str(int(customer_special[1:]) + 1)
        fel_maker(future_event_list, 'Customer Call', state, data, clock,
                  customer_special=next_customer,
                  customer_normal=customer_normal, last_customer='S')

    else:
        next_customer = 'C' + str(int(customer_normal[1:]) + 1)
        fel_maker(future_event_list, 'Customer Call', state, data, clock,
                  customer_special=customer_special,
                  customer_normal=next_customer, last_customer='C')

    # This part is for the customer who has just arrived.
    if last_customer == 'S':
        # Our customer is special
        data['Special Customers'][customer_special] = dict()
        data['Special Customers'][customer_special]['Arrival Time'] = clock
        data['Special Queue Customers All'].add(customer_special)
        if state['Specialist Server Status'] < 2:
            state['Specialist Server Status'] += 1
            fel_maker(future_event_list, 'Departure From Expert', state, data, clock,
                      customer_special=customer_special, customer_normal=customer_normal, last_customer='S')
            data['Special Customers'][customer_special]['Time Service Begins'] = clock
            data['Special Service Starters'].add(customer_special)
        else:
            data['Cumulative Stats']['Area Under Special Queue Length Curve'] += state[
                                                                                     'Special Customer Queue Length'] * (
                                                                                         clock - data[
                                                                                     'Last Time Special Customer Queue Length Changed'])
            state['Special Customer Queue Length'] += 1
            if data['Cumulative Stats']['Max Special Customer Queue Length'] < state[
                'Special Customer Queue Length']:
                data['Cumulative Stats']['Max Special Customer Queue Length'] = state[
                    'Special Customer Queue Length']
            data['Special Queue Customers'][customer_special] = clock
            data['Special Queue Customers All'].add(customer_special)
            data['Last Time Special Customer Queue Length Changed'] = clock
            # will he get tired?
            if Uniform(0, 1) >= 0.85:
                # he will get tired
                fel_maker(future_event_list, 'Leaving Of Tired', state, data, clock,
                          customer_special=customer_special, customer_normal=customer_normal, last_customer='S')

    elif last_customer == "C":
        data['Normal Customers'][customer_normal] = dict()
        data['Normal Customers'][customer_normal]['Arrival Time'] = clock
        data['Normal Queue Customers All'].add(customer_normal)
        if state['Beginner Server Status'] < 3:
            state['Beginner Server Status'] += 1
            fel_maker(future_event_list, 'Departure From Beginner', state, data, clock,
                      customer_special=customer_special, customer_normal=customer_normal, last_customer='C')
            data['Normal Customers'][customer_normal]['Time Service Begins'] = clock
        elif state['Specialist Server Status'] < 2:
            state['Specialist Server Status'] += 1
            fel_maker(future_event_list, 'Departure From Expert', state, data, clock,
                      customer_special=customer_special, customer_normal=customer_normal, last_customer='C')
            data['Normal Customers'][customer_normal]['Time Service Begins'] = clock
        else:
            data['Cumulative Stats']['Area Under Normal Queue Length Curve'] += state[
                                                                                    'Normal Customer Queue Length'] * (
                                                                                        clock - data[
                                                                                    'Last Time Normal Customer Queue Length Changed'])
            state['Normal Customer Queue Length'] += 1
            if data['Cumulative Stats']['Max Normal Customer Queue Length'] < state['Normal Customer Queue Length']:
                data['Cumulative Stats']['Max Normal Customer Queue Length'] = state['Normal Customer Queue Length']
            data['Normal Queue Customers'][customer_normal] = clock
            data['Normal Queue Customers All'].add(customer_normal)
            data['Last Time Normal Customer Queue Length Changed'] = clock
            # will he get tired?
            if Uniform(0, 1) >= 0.85:
                # he will get tired
                fel_maker(future_event_list, 'Leaving Of Tired', state, data, clock,
                          customer_special=customer_special, customer_normal=customer_normal, last_customer='C')


def Departure_From_Expert(future_event_list, state, clock, data, customer_special=None,
                          customer_normal=None,
                          last_customer=None):
    # what is shift number?
    shift = ((clock % 1440) // 480) + 1

    # was it a special or normal customer?
    if last_customer == 'S':
        data['Cumulative Stats']['Specialist Servers Busy Time'] += clock - data['Special Customers'][customer_special][
            'Time Service Begins']
        # data['Special Customers'].pop(customer_special, None)
        # will he use technical service?
        data['Special Customers Waiting Time In System'] += clock - data['Special Customers'][customer_special][
            'Arrival Time']
        if Uniform(0, 1) > 0.85:
            # he will use technical service
            data['Special Customers'][customer_special]['Arrival Time Technical'] = clock
            data['Technical Special Queue Customers All'].add(customer_special)
            if state['Technical Server Status'] < 2:
                # technical service begins immediately
                state['Technical Server Status'] += 1
                fel_maker(future_event_list, 'Departure From Technical', state, data, clock,
                          customer_special=customer_special, customer_normal=customer_normal, last_customer='S')
                data['Special Customers'][customer_special]['Time Service Begins Technical'] = clock
                data['Special Service Starters Technical'].add(customer_special)
            else:
                # gets in line in technical service
                data['Cumulative Stats']['Area Under Technical Special Queue Length Curve'] += state[
                                                                                                   'Technical Special Customer Queue Length'] * (
                                                                                                       clock - data[
                                                                                                   'Last Time Technical Special Customer Queue Length Changed'])
                state['Technical Special Customer Queue Length'] += 1
                if data['Cumulative Stats']['Max Technical Special Customer Queue Length'] < state[
                    'Technical Special Customer Queue Length']:
                    data['Cumulative Stats']['Max Technical Special Customer Queue Length'] = state[
                        'Technical Special Customer Queue Length']
                data['Technical Special Queue Customers'][customer_special] = clock
                data['Technical Special Queue Customers All'].add(customer_special)
                data['Last Time Technical Special Customer Queue Length Changed'] = clock
    else:
        # customer is normal
        data['Cumulative Stats']['Specialist Servers Busy Time'] += clock - data['Normal Customers'][customer_normal][
            'Time Service Begins']
        data['Normal Customers'][customer_normal]['Time Service Ends'] = clock
        # will he use technical service?
        if Uniform(0, 1) > 0.85:
            # he will use technical service
            data['Normal Customers'][customer_normal]['Arrival Time Technical'] = clock
            data['Technical Normal Queue Customers All'].add(customer_normal)
            if state['Technical Server Status'] < 2:
                # technical service begins immediately
                state['Technical Server Status'] += 1
                fel_maker(future_event_list, 'Departure From Technical', state, data, clock,
                          customer_special=customer_special, customer_normal=customer_normal, last_customer='C')
                data['Normal Customers'][customer_normal]['Time Service Begins Technical'] = clock
            else:
                # gets in line in technical service
                data['Cumulative Stats']['Area Under Technical Normal Queue Length Curve'] += state[
                                                                                                  'Technical Normal Customer Queue Length'] * (
                                                                                                      clock - data[
                                                                                                  'Last Time Technical Normal Customer Queue Length Changed'])
                state['Technical Normal Customer Queue Length'] += 1
                if data['Cumulative Stats']['Max Technical Normal Customer Queue Length'] < state[
                    'Technical Normal Customer Queue Length']:
                    data['Cumulative Stats']['Max Technical Normal Customer Queue Length'] = state[
                        'Technical Normal Customer Queue Length']
                data['Technical Normal Queue Customers'][customer_normal] = clock
                data['Technical Normal Queue Customers All'].add(customer_normal)
                data['Last Time Technical Normal Customer Queue Length Changed'] = clock

    # Now after dealing with the customer woh left, wh go further checking the lines.
    if state['Special Customer Queue Length'] > 0:
        # who's the first in line?
        first_customer_in_queue = min(data['Special Queue Customers'], key=data['Special Queue Customers'].get)
        # this customer starts getting service
        data['Special Customers'][first_customer_in_queue]['Time Service Begins'] = clock
        # Update queue waiting time
        data['Cumulative Stats']['Special Queue Waiting Time'] += \
            clock - data['Special Customers'][first_customer_in_queue]['Arrival Time']
        if data['Cumulative Stats']['Max Special Customer Queue Waiting Time'] < clock - \
                data['Special Customers'][first_customer_in_queue]['Arrival Time']:
            data['Cumulative Stats']['Max Special Customer Queue Waiting Time'] = clock - data['Special Customers'][
                first_customer_in_queue]['Arrival Time']
        # Queue length changes, so calculate the area under the current rectangle
        data['Cumulative Stats']['Area Under Special Queue Length Curve'] += \
            state['Special Customer Queue Length'] * (clock - data['Last Time Special Customer Queue Length Changed'])
        state['Special Customer Queue Length'] -= 1
        # This customer no longer belongs to queue
        data['Special Queue Customers'].pop(first_customer_in_queue, None)
        # Queue length just changed. We should update it.
        data['Last Time Special Queue Length Changed'] = clock
        # Schedule its specific 'End of Service'.
        fel_maker(future_event_list, 'Departure From Expert', state, data, clock,
                  customer_special=first_customer_in_queue,
                  customer_normal=customer_normal, last_customer='S')

    elif state['Normal Customer Queue Length'] > 0:
        # who's the first in line?
        first_customer_in_queue = min(data['Normal Queue Customers'], key=data['Normal Queue Customers'].get)
        # this customer starts getting service
        data['Normal Customers'][first_customer_in_queue]['Time Service Begins'] = clock
        # Update queue waiting time
        data['Cumulative Stats']['Normal Queue Waiting Time'] += \
            clock - data['Normal Customers'][first_customer_in_queue]['Arrival Time']
        if data['Cumulative Stats']['Max Normal Customer Queue Waiting Time'] < clock - \
                data['Normal Customers'][first_customer_in_queue]['Arrival Time']:
            data['Cumulative Stats']['Max Normal Customer Queue Waiting Time'] = clock - \
                                                                                 data['Normal Customers'][
                                                                                     first_customer_in_queue][
                                                                                     'Arrival Time']

        # Queue length changes, so calculate the area under the current rectangle
        data['Cumulative Stats']['Area Under Normal Queue Length Curve'] += \
            state['Normal Customer Queue Length'] * (clock - data['Last Time Normal Customer Queue Length Changed'])
        # Logic
        state['Normal Customer Queue Length'] -= 1
        # This customer no longer belongs to queue
        data['Normal Queue Customers'].pop(first_customer_in_queue, None)
        # Queue length just changed. Update 'Last Time Queue Length Changed'
        data['Last Time Normal Queue Length Changed'] = clock
        # Schedule 'End of Service' for this customer
        fel_maker(future_event_list, 'Departure From Expert', state, data, clock,
                  customer_special=customer_special,
                  customer_normal=first_customer_in_queue, last_customer='C')

    else:
        # nothing to do
        state['Specialist Server Status'] -= 1


def Departure_From_Beginner(future_event_list, state, clock, data, customer_special=None,
                            customer_normal=None,
                            last_customer=None):
    # what is shift number
    shift = ((clock % 1440) // 480) + 1

    data['Cumulative Stats']['Beginner Servers Busy Time'] += clock - data['Normal Customers'][customer_normal][
        'Time Service Begins']
    data['Normal Customers'][customer_normal]['Time Service Ends'] = clock

    # will he use technical service?
    if Uniform(0, 1) > 0.85:
        # he will use technical service
        data['Normal Customers'][customer_normal]['Arrival Time Technical'] = clock
        data['Technical Normal Queue Customers All'].add(customer_normal)
        if state['Technical Server Status'] < 2:
            # technical service begins immediately
            state['Technical Server Status'] += 1
            fel_maker(future_event_list, 'Departure From Technical', state, data, clock,
                      customer_special=customer_special, customer_normal=customer_normal, last_customer='C')
            data['Normal Customers'][customer_normal]['Time Service Begins Technical'] = clock
        else:
            # gets in line in technical service
            data['Cumulative Stats']['Area Under Technical Normal Queue Length Curve'] += state[
                                                                                              'Technical Normal Customer Queue Length'] * (
                                                                                                  clock - data[
                                                                                              'Last Time Technical Normal Customer Queue Length Changed'])
            state['Technical Normal Customer Queue Length'] += 1
            if data['Cumulative Stats']['Max Technical Normal Customer Queue Length'] < state[
                'Technical Normal Customer Queue Length']:
                data['Cumulative Stats']['Max Technical Normal Customer Queue Length'] = state[
                    'Technical Normal Customer Queue Length']
            data['Technical Normal Queue Customers'][customer_normal] = clock
            data['Technical Normal Queue Customers All'].add(customer_normal)
            data['Last Time Technical Normal Customer Queue Length Changed'] = clock

    # Now we go to check the lines and other stuff
    if state['Normal Customer Queue Length'] > 0:
        # who's the first in line?
        first_customer_in_queue = min(data['Normal Queue Customers'], key=data['Normal Queue Customers'].get)
        # this customer starts getting service
        data['Normal Customers'][first_customer_in_queue]['Time Service Begins'] = clock
        # Update queue waiting time
        data['Cumulative Stats']['Normal Queue Waiting Time'] += \
            clock - data['Normal Customers'][first_customer_in_queue]['Arrival Time']
        if data['Cumulative Stats']['Max Normal Customer Queue Waiting Time'] < clock - \
                data['Normal Customers'][first_customer_in_queue]['Arrival Time']:
            data['Cumulative Stats']['Max Normal Customer Queue Waiting Time'] = clock - \
                                                                                 data['Normal Customers'][
                                                                                     first_customer_in_queue][
                                                                                     'Arrival Time']
        # Queue length changes, so calculate the area under the current rectangle
        data['Cumulative Stats']['Area Under Normal Queue Length Curve'] += \
            state['Normal Customer Queue Length'] * (clock - data['Last Time Normal Customer Queue Length Changed'])
        state['Normal Customer Queue Length'] -= 1
        # This customer no longer belongs to queue
        data['Normal Queue Customers'].pop(first_customer_in_queue, None)
        # Queue length just changed. Update 'Last Time Queue Length Changed'
        data['Last Time Normal Queue Length Changed'] = clock
        # Schedule its specific 'End of Service' for this customer
        fel_maker(future_event_list, 'Departure From Beginner', state, data, clock,
                  customer_special=customer_special,
                  customer_normal=first_customer_in_queue, last_customer='C')

    else:
        state['Beginner Server Status'] -= 1


def Departure_From_Technical(future_event_list, state, clock, data, customer_special=None,
                             customer_normal=None,
                             last_customer=None):
    if last_customer == 'S':
        data['Cumulative Stats']['Technical Servers Busy Time'] += clock - data['Special Customers'][customer_special][
            'Time Service Begins Technical']
        data['Special Customers Waiting Time In System'] += clock - data['Special Customers'][customer_special][
            'Arrival Time Technical']
    else:
        # customer is normal
        data['Cumulative Stats']['Technical Servers Busy Time'] += clock - data['Normal Customers'][customer_normal][
            'Time Service Begins Technical']
    # now we go check the line
    if state['Technical Special Customer Queue Length'] > 0:
        # who's the first in line?
        first_customer_in_queue = min(data['Technical Special Queue Customers'],
                                      key=data['Technical Special Queue Customers'].get)
        # this customer starts getting service
        data['Special Customers'][first_customer_in_queue]['Time Service Begins Technical'] = clock
        # Update queue waiting time
        data['Cumulative Stats']['Technical Special Queue Waiting Time'] += \
            clock - data['Special Customers'][first_customer_in_queue]['Arrival Time Technical']
        if data['Cumulative Stats']['Max Technical Special Customer Queue Waiting Time'] < clock - \
                data['Special Customers'][first_customer_in_queue]['Arrival Time Technical']:
            data['Cumulative Stats']['Max Technical Special Customer Queue Waiting Time'] = clock - \
                                                                                            data['Special Customers'][
                                                                                                first_customer_in_queue][
                                                                                                'Arrival Time Technical']
        # Queue length changes, so calculate the area under the current rectangle
        data['Cumulative Stats']['Area Under Technical Special Queue Length Curve'] += \
            state['Technical Special Customer Queue Length'] * (
                    clock - data['Last Time Technical Special Customer Queue Length Changed'])
        # Logic
        state['Technical Special Customer Queue Length'] -= 1
        # This customer no longer belongs to queue
        data['Technical Special Queue Customers'].pop(first_customer_in_queue, None)
        # Queue length just changed. Update 'Last Time Queue Length Changed'
        data['Last Time Technical Special Customer Queue Length Changed'] = clock
        # Schedule its specific 'End of Service' for this customer
        fel_maker(future_event_list, 'Departure From Technical', state, data, clock,
                  customer_special=first_customer_in_queue,
                  customer_normal=customer_normal, last_customer='S')

    elif state['Technical Normal Customer Queue Length'] > 0:
        # who's the first in line?
        first_customer_in_queue = min(data['Technical Normal Queue Customers'],
                                      key=data['Technical Normal Queue Customers'].get)
        # this customer starts getting service
        data['Normal Customers'][first_customer_in_queue]['Time Service Begins Technical'] = clock
        # Update queue waiting time
        data['Cumulative Stats']['Technical Normal Queue Waiting Time'] += \
            clock - data['Normal Customers'][first_customer_in_queue]['Arrival Time Technical']
        if data['Cumulative Stats']['Max Technical Normal Customer Queue Waiting Time'] < clock - \
                data['Normal Customers'][first_customer_in_queue]['Arrival Time Technical']:
            data['Cumulative Stats']['Max Technical Normal Customer Queue Waiting Time'] = clock - \
                                                                                           data['Normal Customers'][
                                                                                               first_customer_in_queue][
                                                                                               'Arrival Time Technical']
        # Queue length changes, so calculate the area under the current rectangle
        data['Cumulative Stats']['Area Under Technical Normal Queue Length Curve'] += \
            state['Technical Normal Customer Queue Length'] * (
                    clock - data['Last Time Technical Normal Customer Queue Length Changed'])
        # Logic
        state['Technical Normal Customer Queue Length'] -= 1
        # This customer no longer belongs to queue
        data['Technical Normal Queue Customers'].pop(first_customer_in_queue, None)
        # Queue length just changed. Update 'Last Time Queue Length Changed'
        data['Last Time Technical Normal Customer Queue Length Changed'] = clock
        # Schedule its 'End of Service' for this customer
        fel_maker(future_event_list, 'Departure From Technical', state, data, clock,
                  customer_special=customer_special,
                  customer_normal=first_customer_in_queue, last_customer='C')
    else:
        state['Technical Server Status'] -= 1


def Leaving_Of_Tired(future_event_list, state, clock, data, customer_special=None, customer_normal=None,
                     last_customer=None):
    if last_customer == 'S':
        data['Special Customers Waiting Time In System'] += clock - data['Special Customers'][
            customer_special]['Arrival Time']
        # customer is special
        # here we check if service for this customer has begun
        if 'Time Service Begins' in data['Special Customers'][customer_special].keys():
            # The Service has begun and we do nothing if so.
            True
        else:
            # this customer is one that leaves
            # Update queue waiting time
            data['Cumulative Stats']['Special Queue Waiting Time'] += \
                clock - data['Special Customers'][customer_special]['Arrival Time']
            if data['Cumulative Stats']['Max Special Customer Queue Waiting Time'] < clock - \
                    data['Special Customers'][customer_special]['Arrival Time']:
                data['Cumulative Stats']['Max Special Customer Queue Waiting Time'] = clock - data['Special Customers'][
                    customer_special]['Arrival Time']
            # Queue length changes, so calculate the area under the current rectangle
            data['Cumulative Stats']['Area Under Special Queue Length Curve'] += \
                state['Special Customer Queue Length'] * (
                        clock - data['Last Time Special Customer Queue Length Changed'])
            # Logic
            state['Special Customer Queue Length'] -= 1
            # This customer no longer belongs to queue
            data['Special Queue Customers'].pop(customer_special, None)
            # Queue length just changed. Update 'Last Time Queue Length Changed'
            data['Last Time Special Queue Length Changed'] = clock
            data['Cumulative Stats']['Customer Churn'] += 1
            data['Special Customers'][customer_special]['Leave Time'] = clock


    else:
        # customer is normal
        # here we check if service for this customer has begun
        if 'Time Service Begins' in data['Normal Customers'][customer_normal].keys():
            # The Service has begun and we do nothing if so.
            True
        else:
            # this customer is one that leaves
            # Update queue waiting time
            data['Cumulative Stats']['Normal Queue Waiting Time'] += \
                clock - data['Normal Customers'][customer_normal]['Arrival Time']
            if data['Cumulative Stats']['Max Normal Customer Queue Waiting Time'] < clock - \
                    data['Normal Customers'][customer_normal]['Arrival Time']:
                data['Cumulative Stats']['Max Normal Customer Queue Waiting Time'] = clock - \
                                                                                     data['Normal Customers'][
                                                                                         customer_normal][
                                                                                         'Arrival Time']
            # Queue length changes, so calculate the area under the current rectangle
            data['Cumulative Stats']['Area Under Normal Queue Length Curve'] += \
                state['Normal Customer Queue Length'] * (
                        clock - data['Last Time Normal Customer Queue Length Changed'])
            # Logic
            state['Normal Customer Queue Length'] -= 1
            # This customer no longer belongs to queue
            data['Normal Queue Customers'].pop(customer_normal, None)
            # Queue length just changed. Update 'Last Time Queue Length Changed'
            data['Last Time Normal Queue Length Changed'] = clock
            data['Cumulative Stats']['Customer Churn'] += 1
            data['Normal Customers'][customer_normal]['Leave Time'] = clock






def create_row(step, current_event, state, data, future_event_list):
    sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])

    row = [step, current_event['Event Time'], current_event['Event Type'], current_event['Special Customer'],
           current_event['Normal Customer']]
    row.extend(list(state.values()))
    row.extend(list(data['Cumulative Stats'].values()))
    for event in sorted_fel:
        row.append(event['Event Time'])
        row.append(event['Event Type'])
        row.append(event['Special Customer'])
        row.append(event['Normal Customer'])
    return row


# to create the main part of header
def create_main_header(state, data):
    header = ['Step', 'Clock', 'Event Type', 'Event Special Customer', 'Event Normal Customer']
    header.extend(list(state.keys()))
    header.extend(list(data['Cumulative Stats'].keys()))
    return header


# add blanks to short rows in order to matching lengths to the maximum row length
def justify(table):
    # Find maximum row length in the table
    row_max_len = 0
    for row in table:
        if len(row) > row_max_len:
            row_max_len = len(row)

    # For each row, adding enough blanks
    for row in table:
        row.extend([""] * (row_max_len - len(row)))


def create_excel(table, header):  # To create and fine-tunes the excel output file

    # Find length of each row in the table
    row_len = len(table[0])

    # Find length of header
    header_len = len(header)

    # for each event in the fel with maximum size
    i = 1
    for col in range((row_len - header_len) // 4):
        header.append('Future Event Time ' + str(i))
        header.append('Future Event Type ' + str(i))
        header.append('Future Event Customer Special ' + str(i))
        header.append('Future Event Customer Normal ' + str(i))
        i += 1

    # Dealing with the output

    # create a pandas DataFrame
    df = pd.DataFrame(table, columns=header, index=None)

    # Create a handle to work on the excel file
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

    # Write out the excel file to the hard drive
    df.to_excel(writer, sheet_name='Call Center simulation Output', header=False, startrow=1, index=False)
    workbook = writer.book
    worksheet = writer.sheets['Call Center simulation Output']

    # Create a cell-formatter object
    header_formatter = workbook.add_format()
    # Define the format
    header_formatter.set_align('center')
    header_formatter.set_font('Times New Roman')
    header_formatter.set_bold('True')

    # Write out the column names and apply the format to the cells in the header row
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_formatter)

    # Auto-fit columns
    for i, width in enumerate(get_col_widths(df)):
        worksheet.set_column(i - 1, i - 1, width)

    # Create a cell-formatter object for the body of excel file
    main_formatter = workbook.add_format()
    main_formatter.set_align('center')
    main_formatter.set_align('vcenter')
    main_formatter.set_font('Times New Roman')

    # Apply the format to the body cells
    for row in range(1, len(df) + 1):
        worksheet.set_row(row, None, main_formatter)

    writer.save()  # saving edits


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def simulation(simulation_time):
    state, future_event_list, data = starting_state()
    month = 1
    clock = 0
    table = []
    step = 1
    future_event_list.append(
        {'Event Type': 'End of Simulation', 'Event Time': simulation_time, 'Special Customer': None,
         'Normal Customer': None, 'Last Customer': None})

    while clock < simulation_time:

        sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])

        current_event = sorted_fel[0]
        clock = current_event['Event Time']
        customer_special = current_event['Special Customer']
        customer_normal = current_event['Normal Customer']
        last_customer = current_event['Last Customer']
        if clock < simulation_time:
            if current_event['Event Type'] == 'Customer Call':
                Customer_Call(future_event_list, state, clock, data,
                              customer_special=customer_special,
                              customer_normal=customer_normal, last_customer=last_customer)
            elif current_event['Event Type'] == 'Departure From Expert':
                Departure_From_Expert(future_event_list, state, clock, data,
                                      customer_special=customer_special,
                                      customer_normal=customer_normal, last_customer=last_customer)
            elif current_event['Event Type'] == 'Departure From Beginner':
                Departure_From_Beginner(future_event_list, state, clock, data,
                                        customer_special=customer_special,
                                        customer_normal=customer_normal, last_customer=last_customer)
            elif current_event['Event Type'] == 'Departure From Technical':
                Departure_From_Technical(future_event_list, state, clock, data,
                                         customer_special=customer_special,
                                         customer_normal=customer_normal, last_customer=last_customer)
            elif current_event['Event Type'] == 'Leaving Of Tired':
                Leaving_Of_Tired(future_event_list, state, clock, data,
                                 customer_special=customer_special,
                                 customer_normal=customer_normal, last_customer=last_customer)
            future_event_list.remove(current_event)
        else:
            future_event_list.clear()
        table.append(create_row(step, current_event, state, data, future_event_list))
        step += 1
        # nice_print(state, current_event)

    print('----------------------------------------------------------------------------------')
    # # If you want to run for more than one replication, comment the first three lines of the code below otherwise you may experience a slow run.
    # excel_main_header = create_main_header(state, data)
    # justify(table)
    # create_excel(table, excel_main_header)
    print('Simulation Ended!')
    if data['Technical Special Queue Customers All'] == set():
        data['Technical Special Queue Customers All'] = {-1}
    if data['Technical Normal Queue Customers All'] == set():
        data['Technical Normal Queue Customers All'] = {-1}
    customer_churn = data['Cumulative Stats']['Customer Churn'] / (
                len(data['Special Queue Customers All']) + len(data['Normal Queue Customers All']))


    special_service_starters = (len(
        data['Special Service Starters'].intersection(data['Special Service Starters Technical']))) / (len(
        data['Special Queue Customers All']))
    max_special_customer_queue_length = data['Cumulative Stats']['Max Special Customer Queue Length']
    max_normal_customer_queue_length = data['Cumulative Stats']['Max Normal Customer Queue Length']


    max_special_customer_technical_queue_length = data['Cumulative Stats'][
        'Max Technical Special Customer Queue Length']
    max_normal_customer_technical_queue_length = data['Cumulative Stats']['Max Technical Normal Customer Queue Length']
    mean_special_customer_queue_length = data['Cumulative Stats'][
                                             'Area Under Special Queue Length Curve'] / simulation_time
    mean_normal_customer_queue_length = data['Cumulative Stats'][
                                            'Area Under Normal Queue Length Curve'] / simulation_time
    mean_special_customer_technical_queue_length = data['Cumulative Stats'][
                                                       'Area Under Technical Special Queue Length Curve'] / simulation_time
    mean_normal_customer_technical_queue_length = data['Cumulative Stats'][
                                                      'Area Under Technical Normal Queue Length Curve'] / simulation_time

    max_special_customer_queue_waiting_time = data['Cumulative Stats']['Max Special Customer Queue Waiting Time']
    max_normal_customer_queue_length_waiting_time = data['Cumulative Stats']['Max Normal Customer Queue Waiting Time']

    max_special_customer_technical_queue_waiting_time = data['Cumulative Stats'][
        'Max Technical Special Customer Queue Waiting Time']
    max_normal_customer_technical_queue_waiting_time = data['Cumulative Stats'][
        'Max Technical Normal Customer Queue Waiting Time']
    mean_special_customer_queue_waiting_time = data['Cumulative Stats']['Special Queue Waiting Time'] / len(
        data['Special Queue Customers All'])
    mean_normal_customer_queue_waiting_time = data['Cumulative Stats']['Normal Queue Waiting Time'] / len(
        data['Normal Queue Customers All'])

    mean_special_customer_technical_queue_waiting_time = data['Cumulative Stats'][
                                                             'Technical Special Queue Waiting Time'] / len(
        data['Technical Special Queue Customers All'])
    mean_normal_customer_technical_queue_waiting_time = data['Cumulative Stats'][
                                                            'Technical Normal Queue Waiting Time'] / len(
        data['Technical Normal Queue Customers All'])
    mean_special_customer_waiting_time_in_system = data['Special Customers Waiting Time In System'] / (
        len(data['Special Queue Customers All']))

    specialist_servers_utilization = data['Cumulative Stats']['Specialist Servers Busy Time'] / (2 * simulation_time)
    beginner_servers_utilization = data['Cumulative Stats']['Beginner Servers Busy Time'] / (3 * simulation_time)
    technical_servers_utilization = data['Cumulative Stats']['Technical Servers Busy Time'] / (2 * simulation_time)
    customer_churn_total.append(customer_churn)

    special_service_starters_total.append(special_service_starters)
    max_special_customer_queue_length_total.append(max_special_customer_queue_length)
    max_normal_customer_queue_length_total.append(max_normal_customer_queue_length)
    max_special_customer_technical_queue_length_total.append(max_special_customer_technical_queue_length)
    max_normal_customer_technical_queue_length_total.append(max_normal_customer_technical_queue_length)
    mean_special_customer_queue_length_total.append(mean_special_customer_queue_length)
    mean_normal_customer_queue_length_total.append(mean_normal_customer_queue_length)
    mean_special_customer_technical_queue_length_total.append(mean_special_customer_technical_queue_length)
    mean_normal_customer_technical_queue_length_total.append(mean_normal_customer_technical_queue_length)

    max_special_customer_queue_waiting_time_total.append(max_special_customer_queue_waiting_time)
    max_normal_customer_queue_length_waiting_time_total.append(max_normal_customer_queue_length_waiting_time)
    max_special_customer_technical_queue_waiting_time_total.append(max_special_customer_technical_queue_waiting_time)
    max_normal_customer_technical_queue_waiting_time_total.append(max_normal_customer_technical_queue_waiting_time)
    mean_special_customer_queue_waiting_time_total.append(mean_special_customer_queue_waiting_time)
    mean_normal_customer_queue_waiting_time_total.append(mean_normal_customer_queue_waiting_time)

    # mean_special_customer_again_call_queue_waiting_time_total.append(
    #     mean_special_customer_again_call_queue_waiting_time)
    # mean_normal_customer_again_call_queue_waiting_time_total.append(mean_normal_customer_again_call_queue_waiting_time)
    mean_special_customer_technical_queue_waiting_time_total.append(mean_special_customer_technical_queue_waiting_time)
    mean_normal_customer_technical_queue_waiting_time_total.append(mean_normal_customer_technical_queue_waiting_time)
    mean_special_customer_waiting_time_in_system_total.append(mean_special_customer_waiting_time_in_system)
    specialist_servers_utilization_total.append(specialist_servers_utilization)
    beginner_servers_utilization_total.append(beginner_servers_utilization)
    technical_servers_utilization_total.append(technical_servers_utilization)
    # if you want to have each replication's information, uncomment the code below.
    # print(data['Cumulative Stats']['Beginner Servers Busy Time'])
    # print(f'beginner_servers_utilization is {beginner_servers_utilization}')
    # print(f'customer_churn is {customer_churn}')
    # print(f'special_customers_waiting_time_in_system is {special_customers_waiting_time_in_system}')
    # print(f'special_service_starters is {special_service_starters}')
    # print(f'max_special_customer_queue_length is {max_special_customer_queue_length}')
    # print(f'max_normal_customer_queue_length is {max_normal_customer_queue_length}')
    # print(f'max_special_customer_again_call_queue_length is {max_special_customer_again_call_queue_length}')
    # print(f'max_normal_customer_again_call_queue_length is {max_normal_customer_again_call_queue_length}')
    # print(f'max_special_customer_technical_queue_length is {max_special_customer_technical_queue_length}')
    # print(f'max_normal_customer_technical_queue_length is {max_normal_customer_technical_queue_length}')
    # print(f'mean_special_customer_queue_length is {mean_special_customer_queue_length}')
    # print(f'mean_normal_customer_queue_length is {mean_normal_customer_queue_length}')
    # print(f'mean_special_customer_again_call_queue_length is {mean_special_customer_again_call_queue_length}')
    # print(f'mean_normal_customer_again_call_queue_length is {mean_normal_customer_again_call_queue_length}')
    # print(f'mean_special_customer_technical_queue_length is {mean_special_customer_technical_queue_length}')
    # print(f'mean_normal_customer_technical_queue_length is {mean_normal_customer_technical_queue_length}')
    # print(f'max_special_customer_queue_waiting_time is {max_special_customer_queue_waiting_time}')
    # print(f'max_normal_customer_queue_length_waiting_time is {max_normal_customer_queue_length_waiting_time}')
    # print(f'max_special_customer_again_call_queue_waiting_time is {max_special_customer_again_call_queue_waiting_time}')
    # print(f'max_normal_customer_again_call_queue_waiting_time is {max_normal_customer_again_call_queue_waiting_time}')
    # print(f'max_special_customer_technical_queue_waiting_time is {max_special_customer_technical_queue_waiting_time}')
    # print(f'max_normal_customer_technical_queue_waiting_time is {max_normal_customer_technical_queue_waiting_time}')
    # print(f'mean_special_customer_queue_waiting_time is {mean_special_customer_queue_waiting_time}')
    # print(f'mean_normal_customer_queue_waiting_time is {mean_normal_customer_queue_waiting_time}')
    # print(
    #     f'mean_special_customer_again_call_queue_waiting_time is {mean_special_customer_again_call_queue_waiting_time}')
    # print(f'mean_normal_customer_again_call_queue_waiting_time is {mean_normal_customer_again_call_queue_waiting_time}')
    # print(f'mean_special_customer_technical_queue_waiting_time is {mean_special_customer_technical_queue_waiting_time}')
    # print(f'mean_normal_customer_technical_queue_waiting_time is {mean_normal_customer_technical_queue_waiting_time}')
    # print(f'specialist_servers_utilization is {specialist_servers_utilization}')
    # print(f'beginner_servers_utilization is {beginner_servers_utilization}')
    # print(f'technical_servers_utilization is {technical_servers_utilization}')
    # print(f'mean_special_customer_waiting_time_in_system is {mean_special_customer_waiting_time_in_system}')
    # print(data['Special Customers'])
    # print(data['Normal Customers'])
    # print(data['Special Queue Customers'])
    return data
    print(data)
# simulation(1440)




# if you wanted to run the program so many times and take an average for each result, you may uncomment the bottom code.
# for i in range(100):
#     simulation(43200)
#
# print(sum(customer_churn_total) / len(customer_churn_total))
# print(sum(special_service_starters_total) / len(special_service_starters_total))
# print(sum(max_special_customer_queue_length_total) / len(max_special_customer_queue_length_total))
# print(sum(max_normal_customer_queue_length_total) / len(max_normal_customer_queue_length_total))
# print(sum(max_special_customer_again_call_queue_length_total) / len(max_special_customer_again_call_queue_length_total))
# print(sum(max_normal_customer_again_call_queue_length_total) / len(max_normal_customer_again_call_queue_length_total))
# print(sum(max_special_customer_technical_queue_length_total) / len(max_special_customer_technical_queue_length_total))
# print(sum(max_normal_customer_technical_queue_length_total) / len(max_normal_customer_technical_queue_length_total))
# print(sum(mean_special_customer_queue_length_total) / len(mean_special_customer_queue_length_total))
# print(sum(mean_normal_customer_queue_length_total) / len(mean_normal_customer_queue_length_total))
# print(sum(mean_special_customer_again_call_queue_length_total) / len(mean_special_customer_again_call_queue_length_total))
# print(sum(mean_normal_customer_again_call_queue_length_total) / len(mean_normal_customer_again_call_queue_length_total))
# print(sum(mean_special_customer_technical_queue_length_total) / len(mean_special_customer_technical_queue_length_total))
# print(sum(mean_normal_customer_technical_queue_length_total) / len(mean_normal_customer_technical_queue_length_total))
# print(sum(max_special_customer_queue_waiting_time_total) / len(max_special_customer_queue_waiting_time_total))
# print(sum(max_normal_customer_queue_length_waiting_time_total) / len(max_normal_customer_queue_length_waiting_time_total))
# print(sum(max_special_customer_again_call_queue_waiting_time_total) / len(max_special_customer_again_call_queue_waiting_time_total))
# print(sum(max_normal_customer_again_call_queue_waiting_time_total) / len(max_normal_customer_again_call_queue_waiting_time_total))
# print(sum(max_special_customer_technical_queue_waiting_time_total) / len(max_special_customer_technical_queue_waiting_time_total))
# print(sum(max_normal_customer_technical_queue_waiting_time_total) / len(max_normal_customer_technical_queue_waiting_time_total))
# print(sum(mean_special_customer_queue_waiting_time_total) / len(mean_special_customer_queue_waiting_time_total))
# print(sum(mean_normal_customer_queue_waiting_time_total) / len(mean_normal_customer_queue_waiting_time_total))
# print(sum(mean_special_customer_again_call_queue_waiting_time_total) / len(mean_special_customer_again_call_queue_waiting_time_total))
# print(sum(mean_normal_customer_again_call_queue_waiting_time_total) / len(mean_normal_customer_again_call_queue_waiting_time_total))
# print(sum(mean_special_customer_technical_queue_waiting_time_total) / len(mean_special_customer_technical_queue_waiting_time_total))
# print(sum(mean_special_customer_waiting_time_in_system_total) / len(mean_special_customer_waiting_time_in_system_total))
# print(sum(specialist_servers_utilization_total) / len(specialist_servers_utilization_total))
# print(sum(beginner_servers_utilization_total) / len(beginner_servers_utilization_total))
# print(sum(technical_servers_utilization_total) / len(technical_servers_utilization_total))

num_of_replications = 50
num_of_days = 40
frame_length = 180
window_size = 8
tick_spacing = 40

# Set font and font size
mpl.rc('font', family='Times New Roman')
mpl.rc('font', size=12)

# Create an empty figure with two subplots
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))

# Set up a data structure to save required outputs in each replication
finishing_customers_frame_count = dict()  # keys are replications
waiting_time_frame_aggregate = dict()  # keys are replications


# Function to calculate moving average of a list over a sliding window of length m.
def moving_average(input_list, m):
    output_list = []
    n = len(input_list)
    for i in range(n):
        output_list.append(sum(input_list[max(i - m // 2, 2 * i - n + 1, 0):min(i + m // 2 + 1, 2 * i + 1, n)]) / (
                min(i + m // 2, 2 * i, n - 1) - max(i - m // 2, 2 * i - n + 1, 0) + 1))
    return output_list


# Function to calculate the number of customers who finish getting service in one time-frame
# frame: [start_time, end_time]
def calculate_number_of_finishing_customers(start_time, end_time, customers_data):

    number_of_finishing_customers = 0

    for customer in customers_data:
        # print()
        # print(customers_data[customer])
        if 'Time Service Begins' not in list(customers_data[customer].keys()):
            pass
        elif start_time < customers_data[customer]['Time Service Ends'] <= end_time:
            number_of_finishing_customers += 1
        elif customers_data[customer]['Time Service Ends'] > end_time:
            break

    return number_of_finishing_customers


def calculate_aggregate_queue_waiting_time(start_time, end_time, customers_data):
    cumulative_waiting_time = 0
    for customer in customers_data:
        if 'Time Service Begins' not in list(customers_data[customer].keys()) and 'Leave Time' in list(customers_data[customer].keys()):
            if start_time <= customers_data[customer]['Arrival Time'] < end_time:
                if customers_data[customer]['Leave Time'] < end_time:

                    cumulative_waiting_time += customers_data[customer]['Leave Time'] - \
                                               customers_data[customer]['Arrival Time']
                    # else if the customer will start getting service after this time-frame...
                else:
                    cumulative_waiting_time += end_time - \
                                               customers_data[customer]['Arrival Time']
            elif start_time < customers_data[customer]['Leave Time'] < end_time:

                cumulative_waiting_time += customers_data[customer]['Leave Time'] - \
                                           start_time
        # if the customer has arrived in this time-frame ...
        elif start_time <= customers_data[customer]['Arrival Time'] < end_time:


            if customers_data[customer]['Time Service Begins'] < end_time:

                cumulative_waiting_time += customers_data[customer]['Time Service Begins'] - \
                                           customers_data[customer]['Arrival Time']
            # else if the customer will start getting service after this time-frame...
            else:
                cumulative_waiting_time += end_time - \
                                           customers_data[customer]['Arrival Time']

        # if the customer has arrived before the beginning of this time-frame
        # but starts getting service during this time-frame...
        elif start_time < customers_data[customer]['Time Service Begins'] < end_time:

            cumulative_waiting_time += customers_data[customer]['Time Service Begins'] - \
                                       start_time
        # There might be another (very rare) corner case. What is it? Handle it if you want.

        elif customers_data[customer]['Arrival Time'] > end_time:
            break


    return cumulative_waiting_time


simulation_time = num_of_days * 1440
# Just use the frames with full information (drop last 2 frames)
num_of_frames = simulation_time // frame_length - 3
x = [i for i in range(1, num_of_frames + 1)]

for replication in range(1, num_of_replications + 1):
    simulation_data = simulation(num_of_days * 1440)
    customers_data = simulation_data['Normal Customers']

    finishing_customers_frame_count[replication] = []
    waiting_time_frame_aggregate[replication] = []

    # do calculations frame by frame
    for time in range(0, num_of_frames * frame_length, frame_length):
        finishing_customers_frame_count[replication].append(
            calculate_number_of_finishing_customers(time, time + frame_length, customers_data))

        waiting_time_frame_aggregate[replication].append(
            calculate_aggregate_queue_waiting_time(time, time + frame_length, customers_data))
        calculate_aggregate_queue_waiting_time(time, time + frame_length, customers_data)

finishing_customers_replication_average = []
waiting_time_replication_average = []

for i in range(num_of_frames):
    average_finishing_customers = 0
    average_waiting_time = 0

    for replication in range(1, num_of_replications + 1):
        average_finishing_customers += finishing_customers_frame_count[replication][i] * (1 / num_of_replications)
        average_waiting_time += waiting_time_frame_aggregate[replication][i] * (1 / num_of_replications)

    finishing_customers_replication_average.append(average_finishing_customers)
    waiting_time_replication_average.append(average_waiting_time)

finishing_customers_moving_replication_average = moving_average(finishing_customers_replication_average, window_size)
waiting_time_moving_replication_average = moving_average(waiting_time_replication_average, window_size)

fig.suptitle(f'Warm-up analysis over {num_of_replications} replications')


ax[1].plot(x, waiting_time_replication_average, 'r', linewidth=2, label="Average across replications")
ax[1].plot(x, waiting_time_moving_replication_average, 'k', linewidth=2, label=f'Moving average (m = {window_size})')
ax[1].set_title('Aggregate Waiting Time')
ax[1].set_xlabel('Frame No.')
ax[1].set_ylabel('Aggregate Waiting Time')
ax[1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax[1].legend()

fig.tight_layout()
fig.show()
fig.savefig('Single server queue - Warm-up analysis - Time-Frame Approach')

print('Done!')