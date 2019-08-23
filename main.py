from csv import reader

###THE DATA CLEANING SECTION
### For Google Play data set
opened_file = open('googleplaystore.csv', encoding='utf8')  # utf8 encoding is to avoid UnicodeDecodeError
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

# For App Store Data set
opened_file = open('AppleStore.csv', encoding='utf8')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# Function to show slices of data from any list.
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]

    for row in dataset_slice:
        print(row)
        print('\n')  ###Empty line between rows

    if rows_and_columns:
        print('Number of rows: ', len(dataset))
        print('Number of Columns: ', len(dataset[0]))


"""print(android[10472]) #Section to delete row 10472, error in heading data messes up the duplicate entry check
print(len(android))
del(android[10472])
print(len(android))"""

###Duplicate App Check - only googleplaystore data had this issue
duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

print('Total duplicate apps: ', len(duplicate_apps))
print('\n')

##Loops through app data, reviews column, creates new dict where each key is individual app name,
##Reviews max will keep entries only that have the highest num of ratings compared to their duplicates
reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])

    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

print('Expected Length: ', len(android) - len(duplicate_apps))
print('Actual Length: ', len(reviews_max))

##Removing Duplicate entries of apps, keeping entry with highest num of reviews
android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])

    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


## explore_data(android_clean, 0, 4, True)


##Removal of datasets containing non-english characters
## ASCII Values for all english characters fall into the range of 0-127
## Characters such as ™ or emojis are outside of the ASCII range 0-127, criteria for removal requires 3+ chars outside 0-127

def check_english(string):
    not_ascii = 0

    for char in string:
        if ord(char) > 127:
            not_ascii += 1

    if not_ascii > 3:
        return False
    else:
        return True


print(len(ios))

# Filter out non-english apps for both sets of app data
android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if check_english(name):
        android_english.append(app)

for app in ios:
    name = app[1]
    if check_english(name):
        ios_english.append(app)

### Isolating the free apps only
android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)

for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)

### Length check -
print(len(ios_final), len(ios_english), len(android_final), len(android_english))


# Frequency Table Generator for percentages
def freq_table(dataset, index): #will return a freq table as a dictionary for an column, frequencies in %s
    table = {}
    total = 0

    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1


    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage
    return table_percentages


def display_table(dataset, index): #dataset expected to be list of lists, index an int.
    table = freq_table(dataset, index)
    table_display = []

    for key in table:   #Freq table is turned into a list of tuples
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True) #sorts list of tuples in descending order
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


###Finding most popular apps by genre on the app store using number of installs
###IOS store dataset is missing 'installs' column, will use total number of ratings instead

#generate a freq table for the genres in IOS
ios_genres = freq_table(ios_final, -5)

for genre in ios_genres:
    total = 0  #will store sum of ratings
    genre_length = 0 #will store num of apps per genre
    for app in ios_final:
        app_genre = app[-5] #-5 is the prime_genre category for IOS dataset
        if app_genre == genre:
            n_ratings = float(app[5]) #5 is index for rating_count_tot column of IOS dataset
            total += n_ratings
            genre_length +=1
    avg_n_ratings = total / genre_length
    print(genre, ':', avg_n_ratings,)

for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) #prints name of app and num of ratings

print('\n', 'Android category installs below')
#android_final dataset has number of installs as open ended e.g. '100,000+'. Will convert these to floats
android_categories = freq_table(android_final, 1)

for category in android_categories:
    total = 0
    category_length = 0
    for app in android_final:
        app_category = app[1]
        if app_category == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            category_length += 1
    avg_n_installs = total / category_length
    print(category, ':', avg_n_installs)

