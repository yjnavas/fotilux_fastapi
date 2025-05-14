import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_random_posts(count=10):
    posts = []
    
    for i in range(1, count + 1):
        # Generate random dates within the last year
        created_date = datetime.now() - timedelta(days=random.randint(1, 365))
        updated_date = created_date + timedelta(days=random.randint(0, 30))
        
        # Generate random HTML content for the body
        html_tags = ['<b>', '<i>', '<u>', '<strong>', '<em>']
        random_tag = random.choice(html_tags)
        random_word = fake.word()
        
        body_content = fake.paragraph(nb_sentences=3)
        body_with_html = body_content.replace(random_word, f"{random_tag}{random_word}</{random_tag[1:]}")
        
        # Generate random file name for image
        image_file = f"imagen{random.randint(1, 20)}.jpg"
        
        # Create post with structure matching frontend requirements
        post = {
            "id": i,
            "name": fake.name(),  # This will be replaced with actual user name in API
            "title": fake.sentence(nb_words=random.randint(3, 8)).rstrip('.'),
            "body": body_with_html,
            "userId": random.randint(1, 5),  # Assuming you have users with IDs 1-5
            "createdAt": created_date.isoformat(),
            "updatedAt": updated_date.isoformat(),
            "file": image_file
        }
        
        posts.append(post)
    
    return posts

def get_random_posts_json(count=10):
    posts = generate_random_posts(count)
    return json.dumps(posts, indent=2)

if __name__ == "__main__":
    print(get_random_posts_json())
