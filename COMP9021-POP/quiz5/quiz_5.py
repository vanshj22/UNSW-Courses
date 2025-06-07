# Written by *** for COMP9021
#
# Uses the file cardio_train.csv downloaded from
# https://www.kaggle.com/sulianova/cardiovascular-disease-dataset
#
# Implements a function analyse(gender, age)
# where gender is one of 'F' (for female) or 'M' (for male),
# and where age is any integer for which we have data in the file
# (nothing needs to be done if that is not the case).
#
# We assume that all years have 365 days;
# in particular, someone who is 365 days old is 0 year old,
# and someone who is 366 days old is 1 year old.
#
# We ignore records for which at least one of these conditions holds:
# - height < 150 or height > 200
# - weight < 50 or weight > 150
# - ap_hi < 80 or ap_hi > 200
# - ap_lo < 70 or ap_lo > 140
#
# For each of both classes "cardio problem" and "no cardio problem"
# (as given by the cardio attribute), we create 5 bins/categories for
# height, weight, ap_hi, ap_lo, of equal width,
# that span between smallest value and largest value
# for the attribute in the category.
# For instance, suppose that gender is 'F' and age is 48.
# - Suppose that for the category "cardio problem",
#   the shortest woman aged 48 is 150cm tall, and
#   the tallest woman aged 48 is 200cm tall.
#   Then each of the 5 categories for the class "cardio problem"
#   and for the attribute "height" spans 10cm.
# - Suppose that for the class "no cardio problem",
#   the shortest woman aged 48 is 158cm tall, and
#   the tallest woman aged 48 is 193cm tall.
#   Then each of the 5 categories for the class "no cardio problem"
#   and for the attribute "height" spans 7cm.
# To avoid boundary issues, add 0.1 to the maximum value
# (so with the previous example, the maximum heights would be
# considered to be 200.1 and 193.1, respectively).
# This applies to each of the 4 attributes height, weight,
# ap_hi and ap_lo.
#
# For each attribute and for each of its possible values,
# we compute the ratio of
# - the frequency of people under consideration with a "cardio problem"
#   having that value for that attribute, with
# - the frequency of people under consideration with "no cardio problem"
#   having that value for that attribute.
# Continuing the previous example:
# - Suppose that there are 100 woman aged 48
#   who have a "cardio problem" and 20 of those are at most 160cm tall.
# - Suppose that there are 150 woman aged 48
#   who have "no cardio problem" and 50 of those are at most 165cm tall.
# Then the ratio for the value "category 1" of the attribute "height"
# is 0.2 / 0.3...3...
#
# We keep only ratios that are strictly greater than 1 and order them
# from largest to smallest.
# A ratio might be infinite (see second sample test).
# In case two ratios are exactly the same, their order is determined
# by the order of the corresponding attributes in the csv file
# (first is height, last is being active or not), and in case the
# attributes are the same, their order is determined by the rank of
# the category (first is 1, last is 5; for booleans, False comes
# before True).
#
# We format ratios with 2 digits after the decimal point.
# After a ratio, the output is one of:
# - Height in category [1-5] (1 lowest, 5 highest)
# - Weight in category [1-5] (1 lowest, 5 highest)
# - Systolic blood pressure in category [1-5] (1 lowest, 5 highest)
# - Diastolic blood pressure in category [1-5] (1 lowest, 5 highest)
# - Cholesterol in category [1-3] (1 lowest, 3 highest)
# - Glucose in category [1-3] (1 lowest, 3 highest)
# - Smoking/Not smoking
# - Drinking/Not drinking
# - Not being active/Being active
#
# You are NOT allowed to use pandas. If you do, then your submission
# will NOT be assessed and you will score 0 to the quiz.


# gender = 1 - F(Female), 2 - M(Male)
# age in days, 1 yr = 365 days    365 days old is 0 year old, 366 days old is 1 year old.
#  TARGET = cardio => 1 present, 0 absent

import csv
from collections import defaultdict
from pathlib import Path


def read_csv_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        data = [row for row in reader]
    return data

def filter_data(data, gender, age):
    filtered_data = []
    if gender =='F':
        gender = 1
    elif gender == 'M':
        gender = 2
    else:
        return False
    
    for record in data:
        record['id'] = int(record['id'])
        record['age'] = int(record['age'])
        record['gender'] = int(record['gender'])
        record['height'] = int(record['height'])
        record['weight'] = float(record['weight'])
        record['ap_hi'] = int(record['ap_hi'])
        record['ap_lo'] = int(record['ap_lo'])
        record['cholesterol'] = int(record['cholesterol'])
        record['gluc'] = int(record['gluc'])
        record['smoke'] = int(record['smoke'])
        record['alco'] = int(record['alco'])
        record['active'] = int(record['active'])
        record['cardio'] = int(record['cardio'])
        
        if calculate_age(record['age']) != age or record['gender'] != gender:
            continue
        
        # Height, weight, ap_hi, ap_lo data filtering
        if not ( record['height'] < 150 or record['height'] > 200 or
            record['weight'] < 50 or record['weight'] > 150 or
            record['ap_hi'] < 80 or record['ap_hi'] > 200  or
            record['ap_lo'] < 70 or record['ap_lo'] > 140):

            filtered_data.append(record)

    return filtered_data

def create_bins(attributes, num_bins):
    if num_bins == 2:
        return [(min(attributes), max(attributes)), (max(attributes), max(attributes) + 0.1)]
    if num_bins == 3:
        return [(1, 2), (2, 3), (3, 3.1)]
    else:
        min_val = min(attributes)
        max_val = max(attributes) + 0.1   # Add 0.1 for boundary issues

        bin_width = (max_val - min_val) / num_bins
        bins = []

        for i in range(num_bins):
            bins.append((min_val + i * bin_width, min_val + (i + 1) * bin_width))
        return bins

def compute_ratios(cardio_counts, no_cardio_counts):
    ratios = {}
    sum_cardio_counts = sum(cardio_counts.values())
    sum_no_cardio_counts = sum(no_cardio_counts.values())

    for category in cardio_counts:
        cardio_count = cardio_counts.get(category, 0)
        no_cardio_count = no_cardio_counts.get(category, 0)
        if no_cardio_count == 0: 
            ratios[category] = float('inf')  # Infinite ratio
        else:
            ratio = (cardio_count/sum_cardio_counts )/ (no_cardio_count/sum_no_cardio_counts)
            # if ratio > 1:  # Keep only ratios greater than 1
            ratios[category] = ratio
        # if no_cardio_count > 0:  # Avoid division by zero
        #     ratio = (cardio_count/sum_cardio_counts )/ (no_cardio_count/sum_no_cardio_counts)
        #     if ratio > 1:  # Keep only ratios greater than 1
        #         ratios[category] = ratio
    return ratios

def calculate_age(days):
    return -(days//-365)-1

def categorize_records(records, bins, attribute):
    counts = defaultdict(int)
    for record in records:
        value = record[attribute]
        for i, (lower, upper) in enumerate(bins):
            if lower <= value < upper:
                counts[i + 1] += 1  # Category starts from 1
                break
    return counts

def analyse(gender, age):
    # column_headers = ['id', 'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']
    # attributes_1 = ['height', 'weight', 'ap_hi', 'ap_lo']
    bin_values = {'height': 5, 'weight': 5, 'ap_hi': 5, 'ap_lo': 5, 'cholesterol': 3, 'gluc': 3, 'smoke': 2, 'alco': 2, 'active': 2}
    full_forms = {'height': 'Height', 'weight':'Weight', 'ap_hi':'Systolic blood pressure', 'ap_lo': 'Diastolic blood pressure', 'gluc': 'Glucose', 'smoke': 'smoking', 'alco': 'drinking', 'active': 'being active'}

    data_path = Path('quiz5/cardio_train.csv') # remove quiz5
    if data_path.exists(): # check if file exits 
        data = read_csv_data(data_path)

    filtered_data = filter_data(data, gender, age)

    cardio_records = [record for record in filtered_data if record['cardio'] == 1]
    no_cardio_records = [record for record in filtered_data if record['cardio'] == 0]


    results = []
    for attribute, bin_value in bin_values.items():
        # print()
        cardio_bins = create_bins([record[attribute] for record in cardio_records], bin_value)
        cardio_counts = categorize_records(cardio_records, cardio_bins, attribute)
        
        no_cardio_bins = create_bins([record[attribute] for record in no_cardio_records], bin_value)
        no_cardio_counts = categorize_records(no_cardio_records, no_cardio_bins, attribute)

        ratios = compute_ratios(cardio_counts, no_cardio_counts)

        for category, ratio in ratios.items():
            if ratio > 1:
                if bin_value == 5:
                    results.append((ratio, f"{full_forms[attribute] if attribute in full_forms else attribute.capitalize() } in category {category} (1 lowest, 5 highest)"))
                elif bin_value == 3:
                    results.append((ratio, f"{full_forms[attribute] if attribute in full_forms else attribute.capitalize()} in category {category} (1 lowest, 3 highest)"))
                elif attribute == 'active':
                    results.append((ratio, f"{full_forms[attribute].capitalize() if category== 2 else 'Not ' + full_forms[attribute] }"))                
                else:
                    results.append((ratio, f"{full_forms[attribute].capitalize() if category== 1 else 'Not ' + full_forms[attribute] }"))
                

    results.sort(reverse=True, key=lambda x: (x[0], x[1]))

    print(f"The following might particularly contribute to cardio problems for {'females' if gender == 'F' else 'males'} aged {age}:")
    for ratio, description in results:
        print(f"   {ratio:.2f}: {description}")

if __name__ == '__main__':
    analyse('F', 43)
    # analyse('M', 58)


