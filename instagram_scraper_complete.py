# from instagram_private_api import Client, ClientCompatPatch


# from dotenv import load_dotenv
# import os

# # Load the environment variables from the .env file
# load_dotenv()

# # Use the environment variables to set the values of your variables
# YOUR_USERNAME = os.getenv('INSTAGRAM_USERNAME')
# YOUR_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# user_name = os.getenv('INSTAGRAM_USERNAME')
# password = os.getenv('INSTAGRAM_PASSWORD')

# api = Client(user_name, password)
# results = api.feed_timeline()
# items = [item for item in results.get('feed_items', [])
#          if item.get('media_or_ad')]
# for item in items:
#     # Manually patch the entity to match the public api as closely as possible, optional
#     # To automatically patch entities, initialise the Client with auto_patch=True
#     ClientCompatPatch.media(item['media_or_ad'])
#     print(item['media_or_ad']['code'])



from instagram_private_api import Client, ClientError
import matplotlib.pyplot as plt
import uuid

from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Use the environment variables to set the values of your variables
YOUR_USERNAME = os.getenv('INSTAGRAM_USERNAME')
YOUR_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
INFLUENCER = os.getenv('INFLUENCER_NAME')

# Replace YOUR_USERNAME and YOUR_PASSWORD with your Instagram login credentials
api = Client(YOUR_USERNAME, YOUR_PASSWORD)


# Define a function to retrieve the followers of an influencer
def get_followers(api, user_id):
  followers = []
  # Generate a rank_token
  # rank_token = generate_uuid()
  rank_token = str(uuid.uuid4())
  # Use the api.user_followers method to retrieve a list of the influencer's followers
  result = api.user_followers(user_id, rank_token=rank_token)
  followers.extend(result.get('users', []))
  # Check if there are more followers to retrieve
  next_max_id = result.get('next_max_id')
  while next_max_id:
    # If there are more followers, retrieve the next batch
    result = api.user_followers(user_id, max_id=next_max_id, rank_token=rank_token)
    followers.extend(result.get('users', []))
    next_max_id = result.get('next_max_id')
  return followers

# Define a function to process the followers data
def process_followers(followers):
  # Process the data to extract the information you are interested in
  # For example, you could count the number of followers in each age group or gender
  age_counts = {}
  gender_counts = {}
  for follower in followers:
    # Extract the follower's age and gender from their profile
    age = follower.get('age', 'unknown')
    print('Age is', age)
    gender = follower.get('gender', 'unknown')
    print('Gender is', gender)
    # gender = follower['gender']
    profile_pic_url = follower['profile_pic_url']

    # Print the profile picture URL
    print('Profile picture URL:', profile_pic_url)
    
    # Increment the count for the appropriate age group or gender
    if age not in age_counts:
      age_counts[age] = 0
    age_counts[age] += 1
    if gender not in gender_counts:
      gender_counts[gender] = 0
    gender_counts[gender] += 1
  return age_counts, gender_counts

#
# Replace INFLUENCER_USERNAME with the username of the influencer whose data you want to access
user_id = api.username_info(INFLUENCER)['user']['pk']

# Retrieve the followers of the influencer
followers = get_followers(api, user_id)

# Process the followers data
age_counts, gender_counts = process_followers(followers)

# Print the results
print('Age counts:', age_counts)
print('Gender counts:', gender_counts)

# You could also visualize the data using libraries like matplotlib or seaborn

# Create a bar chart showing the number of followers in each age group
plt.bar(age_counts.keys(), age_counts.values())
plt.xlabel('Age')
plt.ylabel('Number of followers')
plt.title('Followers by age')
plt.show()

# Create a pie chart showing the percentage of followers in each gender
plt.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%')
plt.title('Followers by gender')
plt.show()
