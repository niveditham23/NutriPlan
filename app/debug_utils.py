from app import db
from app.models import User,UserInfo,MealData,PersonalMealData
import datetime

# from app.views import user_info


def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'full_name': 'Amy Green',   'email': 'amy@b.com', 'pw': 'Amy@7890'},
        {'full_name': 'Tom Holland',   'email': 'tom@b.com', 'pw': 'Tom@7890'},
        {'full_name': 'Yin Guang',   'email': 'yin@b.com', 'pw': 'Yin@7890'},
        {'full_name': 'Sarah Shines', 'email': 'sarah@b.com', 'pw': 'Sarah@7890'},
        {'full_name': 'Joe Keery',    'email': 'joe@b.com',  'pw': 'Joe@7890'},
    ]

    user_infos = [
        {'age': 28, 'gender': 'female', 'height': 165, 'weight': 60, 'diet_type': 'vegan', 'allergies': 'gluten,nuts','health_conditions': 'pcos', 'primary_goal': 'maintain', 'activity_level': 'lightlyactive'},
        {'age': 35, 'gender': 'male', 'height': 180, 'weight': 80, 'diet_type': 'non-veg', 'allergies': None,'health_conditions': 'diabetes', 'primary_goal': 'lose', 'activity_level': 'moderatelyactive'},
        {'age': 42, 'gender': 'male', 'height': 170, 'weight': 70, 'diet_type': 'keto', 'allergies': 'soya','health_conditions': 'thyroid', 'primary_goal': 'gain', 'activity_level': 'sedentary'},
        {'age': 30, 'gender': 'female', 'height': 175, 'weight': 75, 'diet_type': 'mediterranean', 'allergies': 'peanuts','health_conditions': None, 'primary_goal': 'maintain', 'activity_level': 'very_active'},
        {'age':37, 'gender': 'male', 'height': 175, 'weight': 75, 'diet_type': 'mediterranean', 'allergies': 'peanuts','health_conditions':None, 'primary_goal': 'maintain', 'activity_level': 'very_active'}

    ]

    for u,info in zip(users,user_infos):
        pw = u.pop('pw')
        user = User(**u)
        user.set_password(pw)
        db.session.add(user)
        db.session.flush()
        info_obj=UserInfo(user_id=user.id,**info)
        db.session.add(info_obj)

    meals=[{
    "meal_type": "Breakfast",
    "meal_name": "Oats with Fruits",
    "calories": 300,
    "recipe": """
    Ingredients:
    - ½ cup rolled oats
    - 1 cup milk (or plant-based)
    - ½ banana, ¼ cup berries, ½ apple
    - 1 tbsp seeds/nuts, optional cinnamon

    Instructions:
    1. Cook oats in milk until creamy.
    2. Top with fruits and seeds before serving.
    """,
    "diet_type": ["vegetarian", "vegan"],
    "allergens": ["Milk", "Tree nuts"] ,
    "health_conditions": ["diabetes", "pcos"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Avocado Toast",
    "calories": 250,
    "recipe": """
    Ingredients:
    - 1 slice whole grain bread
    - 1 ripe avocado
    - Salt, lemon juice, chili flakes

    Instructions:
    1. Toast bread and mash avocado with seasonings.
    2. Spread on toast. Add toppings if desired.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": ["Wheat"],
    "health_conditions": ["thyroid", "pcos"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Scrambled Eggs with Spinach",
    "calories": 320,
    "recipe": """
    Ingredients:
    - 2 eggs, handful spinach
    - 1 tsp olive oil, salt & pepper

    Instructions:
    1. Sauté spinach and add whisked eggs.
    2. Scramble until cooked through.
    """,
    "diet_type": ["vegetarian"],
    "allergens": ["Eggs"],
    "health_conditions": ["thyroid", "diabetes"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Chia Pudding",
    "calories": 280,
    "recipe": """
    Ingredients:
    - 2 tbsp chia seeds
    - ½ cup almond milk
    - 1 tsp honey, berries for topping

    Instructions:
    1. Mix chia seeds with milk and refrigerate overnight.
    2. Top with fruits before serving.
    """,
    "diet_type": ["vegan", "vegetarian", "keto"],
    "allergens": ["Tree nuts"],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Greek Yogurt with Berries",
    "calories": 290,
    "recipe": """
    Ingredients:
    - 1 cup Greek yogurt
    - ½ cup mixed berries
    - 1 tsp chia or flax seeds

    Instructions:
    1. Mix yogurt with berries and seeds.
    2. Chill and serve.
    """,
    "diet_type": ["vegetarian", "mediterranean"],
    "allergens": ["Milk"],
    "health_conditions": ["diabetes"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Peanut Butter Banana Toast",
    "calories": 350,
    "recipe": """
    Ingredients:
    - 1 slice whole grain bread
    - 1 tbsp peanut butter
    - ½ banana, sliced

    Instructions:
    1. Toast bread, spread peanut butter.
    2. Top with banana slices.
    """,
    "diet_type": ["vegetarian"],
    "allergens": ["Peanuts", "Wheat"],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Tofu Scramble",
    "calories": 330,
    "recipe": """
    Ingredients:
    - ½ block firm tofu, crumbled
    - ¼ cup bell pepper, spinach
    - Turmeric, salt, pepper

    Instructions:
    1. Sauté veggies and tofu until browned.
    2. Season with turmeric and spices.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": ["Soy"],
    "health_conditions": ["thyroid"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Protein Smoothie",
    "calories": 310,
    "recipe": """
    Ingredients:
    - 1 scoop protein powder
    - 1 banana, 1 tbsp peanut butter
    - 1 cup almond milk

    Instructions:
    1. Blend all ingredients until smooth.
    2. Serve chilled.
    """,
    "diet_type": ["vegan", "vegetarian", "paleo"],
    "allergens": ["Peanuts", "Tree nuts"],
    "health_conditions": ["diabetes"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Boiled Eggs with Veggies",
    "calories": 270,
    "recipe": """
    Ingredients:
    - 2 boiled eggs
    - ¼ cup cucumber, tomato, and carrot sticks

    Instructions:
    1. Boil eggs and slice veggies.
    2. Serve together with light seasoning.
    """,
    "diet_type": ["vegetarian", "keto"],
    "allergens": ["Eggs"],
    "health_conditions": ["thyroid", "pcos"]
},
{
    "meal_type": "Breakfast",
    "meal_name": "Almond Butter Oatmeal",
    "calories": 350,
    "recipe": """
    Ingredients:
    - ½ cup oats
    - 1 cup almond milk
    - 1 tbsp almond butter, cinnamon

    Instructions:
    1. Cook oats in almond milk.
    2. Stir in almond butter and cinnamon before serving.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": ["Tree nuts"],
    "health_conditions": ["diabetes"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Grilled Chicken Salad",
    "calories": 400,
    "recipe": """
    Ingredients:
    - 1 grilled chicken breast
    - 1 cup lettuce
    - ½ cup cherry tomatoes
    - ¼ cucumber, sliced
    - 1 tbsp olive oil, salt, pepper

    Instructions:
    1. Slice grilled chicken and vegetables.
    2. Toss everything with olive oil and season to taste.
    """,
    "diet_type": ["paleo", "keto", "mediterranean"],
    "allergens": [],
    "health_conditions": ["diabetes", "pcos"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Quinoa Chickpea Bowl",
    "calories": 450,
    "recipe": """
    Ingredients:
    - ½ cup cooked quinoa
    - ½ cup canned chickpeas
    - ¼ cup chopped cucumber & tomato
    - 1 tbsp lemon juice, parsley, olive oil

    Instructions:
    1. Combine all ingredients in a bowl.
    2. Drizzle with lemon juice and olive oil, then toss.
    """,
    "diet_type": ["vegan", "vegetarian", "mediterranean"],
    "allergens": [],
    "health_conditions": ["thyroid", "pcos"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Lentil Soup & Side Salad",
    "calories": 420,
    "recipe": """
    Ingredients:
    - ½ cup red lentils
    - ½ chopped onion, ½ carrot, 1 celery stalk
    - 2 cups water or broth, salt, cumin

    Instructions:
    1. Sauté veggies, add lentils and water, cook until soft.
    2. Blend slightly if desired, and serve with salad.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": ["Celery"],
    "health_conditions": ["diabetes", "thyroid"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Grilled Tofu Wrap",
    "calories": 470,
    "recipe": """
    Ingredients:
    - ½ cup grilled tofu
    - 1 whole wheat wrap
    - ¼ cup shredded carrots and lettuce
    - 1 tbsp hummus or tahini

    Instructions:
    1. Spread hummus on wrap, fill with tofu and veggies.
    2. Roll and grill lightly for a warm wrap.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": ["Soy", "Wheat", "Sesame"],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Salmon & Steamed Veggies",
    "calories": 500,
    "recipe": """
    Ingredients:
    - 1 salmon fillet
    - ½ cup broccoli, ½ cup carrots
    - 1 tbsp olive oil, herbs, salt

    Instructions:
    1. Bake or grill salmon with herbs and oil.
    2. Steam veggies and serve together.
    """,
    "diet_type": ["paleo", "mediterranean"],
    "allergens": ["Fish"],
    "health_conditions": ["thyroid", "diabetes"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Falafel Salad Bowl",
    "calories": 440,
    "recipe": """
    Ingredients:
    - 3 baked falafels
    - 1 cup greens
    - ½ cup tomato & cucumber
    - 1 tbsp tahini dressing

    Instructions:
    1. Arrange salad and add warm falafels.
    2. Drizzle tahini and serve.
    """,
    "diet_type": ["vegan", "vegetarian", "mediterranean"],
    "allergens": ["Sesame"],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Zucchini Noodles with Pesto",
    "calories": 380,
    "recipe": """
    Ingredients:
    - 1 medium zucchini (spiralized)
    - 2 tbsp pesto sauce
    - ¼ cup cherry tomatoes

    Instructions:
    1. Sauté zoodles for 2 mins, stir in pesto.
    2. Top with tomatoes and serve.
    """,
    "diet_type": ["vegetarian", "keto"],
    "allergens": ["Tree nuts"],
    "health_conditions": ["thyroid"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Stuffed Bell Peppers",
    "calories": 450,
    "recipe": """
    Ingredients:
    - 2 bell pepper, halved
    - ½ cup cooked quinoa
    - ¼ cup black beans, corn, tomato sauce

    Instructions:
    1. Mix quinoa and veggies, fill peppers.
    2. Bake for 20 mins until soft.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": [],
    "health_conditions": ["diabetes", "pcos"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Turkey Lettuce Wraps",
    "calories": 390,
    "recipe": """
    Ingredients:
    - ½ cup ground turkey
    - 1 garlic clove, lettuce leaves
    - 1 tsp soy sauce, lime juice

    Instructions:
    1. Cook turkey with garlic and soy.
    2. Spoon into lettuce, top with lime.
    """,
    "diet_type": ["paleo", "keto"],
    "allergens": ["Soy"],
    "health_conditions": ["diabetes"]
},
{
    "meal_type": "Lunch",
    "meal_name": "Avocado Chickpea Sandwich",
    "calories": 460,
    "recipe": """
    Ingredients:
    - ½ avocado, ¼ cup mashed chickpeas
    - Salt, lemon, 2 slices whole grain bread

    Instructions:
    1. Mix avocado and chickpeas with lemon.
    2. Spread on bread and serve.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": ["Wheat"],
    "health_conditions": ["pcos"]
}, {
    "meal_type": "Dinner",
    "meal_name": "Grilled Veggie Bowl",
    "calories": 410,
    "recipe": """
    Ingredients:
    - ½ cup grilled zucchini, bell pepper, and mushroom
    - ½ cup brown rice
    - 1 tbsp tahini or hummus

    Instructions:
    1. Grill vegetables and cook rice.
    2. Serve with tahini drizzle.
    """,
    "diet_type": ["vegan", "vegetarian", "mediterranean"],
    "allergens": ["Sesame"],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Baked Cod with Asparagus",
    "calories": 430,
    "recipe": """
    Ingredients:
    - 1 cod fillet
    - 5–6 asparagus stalks
    - Lemon juice, herbs, olive oil

    Instructions:
    1. Bake cod and asparagus with herbs and oil.
    2. Serve with lemon wedge.
    """,
    "diet_type": ["paleo", "mediterranean"],
    "allergens": ["Fish"],
    "health_conditions": ["thyroid", "diabetes"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Chickpea Curry with Rice",
    "calories": 500,
    "recipe": """
    Ingredients:
    - ½ cup chickpeas
    - ¼ cup onion, tomato, garlic
    - ½ cup brown rice, spices

    Instructions:
    1. Cook curry base and add chickpeas.
    2. Simmer and serve with rice.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": [],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Stuffed Zucchini Boats",
    "calories": 390,
    "recipe": """
    Ingredients:
    - 2 zucchini, halved
    - ¼ cup ground turkey or tofu
    - Tomato sauce, herbs, garlic

    Instructions:
    1. Hollow and stuff zucchini, top with sauce.
    2. Bake for 20 mins at 180°C.
    """,
    "diet_type": ["paleo", "vegetarian", "keto"],
    "allergens": [],
    "health_conditions": ["diabetes", "pcos"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Quinoa & Black Bean Bowl",
    "calories": 460,
    "recipe": """
    Ingredients:
    - ½ cup cooked quinoa
    - ½ cup black beans
    - Corn, avocado, lime

    Instructions:
    1. Combine all ingredients.
    2. Add lime juice and serve.
    """,
    "diet_type": ["vegan", "vegetarian", "mediterranean"],
    "allergens": [],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Cauliflower Fried Rice",
    "calories": 380,
    "recipe": """
    Ingredients:
    - 1 cup cauliflower rice
    - ¼ cup peas and carrots
    - 1 egg or tofu, soy sauce

    Instructions:
    1. Sauté veggies and protein.
    2. Add cauliflower rice and stir-fry.
    """,
    "diet_type": ["vegetarian", "keto"],
    "allergens": ["Soy", "Eggs"],
    "health_conditions": ["diabetes"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Shrimp & Veggie Skewers",
    "calories": 420,
    "recipe": """
    Ingredients:
    - 6 shrimp, ½ cup bell peppers, onion
    - Lemon, garlic, olive oil

    Instructions:
    1. Thread ingredients on skewers and grill.
    2. Drizzle lemon and serve.
    """,
    "diet_type": ["paleo", "mediterranean"],
    "allergens": ["Shellfish"],
    "health_conditions": ["thyroid"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Eggplant Lasagna",
    "calories": 460,
    "recipe": """
    Ingredients:
    - 1 eggplant, sliced
    - ½ cup marinara, ¼ cup cheese or vegan cheese

    Instructions:
    1. Layer eggplant and sauce, bake until bubbly.
    2. Top with cheese and serve.
    """,
    "diet_type": ["vegetarian", "keto"],
    "allergens": ["Milk"],
    "health_conditions": ["pcos"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Tofu Stir-Fry",
    "calories": 400,
    "recipe": """
    Ingredients:
    - ½ block tofu, cubed
    - ¼ cup broccoli, bell pepper
    - Soy sauce, garlic, sesame oil

    Instructions:
    1. Stir-fry tofu and veggies.
    2. Add sauce and cook until tender.
    """,
    "diet_type": ["vegan", "vegetarian"],
    "allergens": ["Soy", "Sesame"],
    "health_conditions": ["diabetes"]
},
{
    "meal_type": "Dinner",
    "meal_name": "Chicken Zoodle Alfredo",
    "calories": 450,
    "recipe": """
    Ingredients:
    - 1 cup spiralized zucchini
    - ½ cup cooked chicken
    - ¼ cup alfredo sauce (dairy or vegan)

    Instructions:
    1. Cook chicken and toss with zoodles.
    2. Stir in sauce and warm gently.
    """,
    "diet_type": ["paleo", "keto"],
    "allergens": ["Milk"] ,
    "health_conditions": ["thyroid"]}
]

    def serialize_meal_data(meal: dict) -> dict:
        return {
            'meal_type': meal['meal_type'],
            'meal_name': meal['meal_name'],
            'calories': meal['calories'],
            'recipe': meal['recipe'],
            'diet_type': ', '.join(meal['diet_type']) if isinstance(meal['diet_type'], list) else meal['diet_type'],
            'allergens': ', '.join(meal['allergens']) if isinstance(meal['allergens'], list) else meal['allergens'],
            'health_conditions': ', '.join(meal['health_conditions']) if isinstance(meal.get('health_conditions'),list) else meal.get('health_conditions',''),
        }

    for meal in meals:
        serialized_meal = serialize_meal_data(meal)
        meal_obj = MealData(**serialized_meal)
        db.session.add(meal_obj)
    db.session.commit()