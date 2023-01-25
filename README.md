You are the head chef at a hotel. At this hotel, 4 meals a day are provided to guests: breakfast, lunch, dinner, and afternoon snack. Some meals can serve more than one role: for example a BLT sandwich can be breakfast, lunch, or an afternoon snack. Given a 'menu' of possible meals generate all valid permutations of meals that could be served to guests.

**Complication:** guests demand variety in their diet. We can assign 'variety' a number based on the number of times in 1 day the same meal is repeated. For example, guests may only tolerate having the same meal twice in 2 days - this would be a value of 1.

**Complication 2:** each meal has a fixed set of ingredients but ingredients might be shared between them. How many of each ingredient do you need to order to execute your menu? How can we minimise ingredients / potential cost of ingredients?

**Complication 3:** meals only last a fixed amount of time (defined as number of timeslots) before they must be thrown away, wasting money. **I feel like this either reduces to the variety complication or introduces the issue of the real amount of food consumed, which requires more depth, i.e. it's a separate complication and isn't a planning problem.**

**Complication 4:** monetary cost associated with preparing different meals and optimising for minimal cost.

**Example:**
In this example there are no complications.
You have a menu with 2 options: a portion of fries, which can be served as any meal, or a sandwich, which can only be served as breakfast, lunch, or snack.
Any combination of meals is valid in this case. You can serve `7*4=28` portions of fries, or any combination of meals which adds up to 28 meals in total.

## Analysis

### Basic Case

It's trivial to represent the menu of possible meals as a matrix where B is breakfast, L lunch, D dinner, S snack:

```
        B L D S
Meal 1: 1 0 1 0
Meal 2: 1 1 1 0
Meal 3: 0 0 1 1
```

If any column has only 0 then there is no solution. Otherwise a solution should be possible.

In the basic case the *total* minimum number of meals is always `4x7=28` with different permutations depending on the specifics of the matrix (this is an interesting problem to explore in itself.) Take a basic example:

```
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
```

In this case we can see that we just need to prepare 7 breakfasts, 7 lunches, 7 dinners, and 7 snacks.

With different complications this becomes more challenging to solve and the total number of meals needed may vary.

### Complication 1: Variety

In order to model variety, we need two additional variables. One is the length of time variety is demanded over (expressed in either days or timeslots where a day is 4 slots). Let this be called `period`. The other is the number of times guests are willing to accept the same meal in that time period. Let this be called `repetitions`.

E.g. if guests demand that they have 4 different meals per day:
```
period = 1
repetitions = 1
```
This could also be expressed as `1:1` .
If guests demand a meal repeats only 3 times in a 3-day period, this would be `3:3`.
If they tolerate 2 of the same meal in one day, it's `1:2`.

An additional variable would be consecutive meals: it may be true that guests tolerate 2 of the same meal in a day, but they will not tolerate the same meal for breakfast and lunch. This might be able to be modelled effectively through the same schema if timeslots rather than days were used as a unit.

Note that numerous constraints could apply at once.

Finally, we could have variety apply only to certain types of meal (but probably not specific meals). For example, breakfast could be `7:3` (the same breakfast is tolerated 3 days of the week), while dinner could be `7:1` (no repetitions of the same dinner are tolerated at all).

Do we want / need to generate an actual timetable for this? This appears to be a flavour of the timetabling problem.

### Complication 2: Ingredients

This seems to be another level of abstraction provided to the original problem.
Let `ingredient_num` be the number of different ingredients in total for all recipes.
Let `meal_num` be the number of different meals.
Now we can represent the meals' ingredients in another matrix: here each row is a meal type, each column is an ingredient type, and each cell is the number of ingredients needed for that meal type. The array is of dimensions `ingredient_num x meal_num`

```
2 3 4 0 0 // meal 1
0 0 0 1 1 // meal 2
0 2 1 0 0 // meal 3
```

When multiplied with the number of each meal, this gives the total number of ingredients used in the recipe.

We want to minimise something here: either the variety of ingredients, the total number of units of ingredients used, or more likely the price of ingredients (see complication 3). We can consider minimising units to be a simplified pricing problem (i.e. 1 unit of an ingredient is set to have value 1).

### Complication 3: Prices

This can apply to either the simpler problem (meal optimisation) or the more complex problem (ingredients). In the former case each meal has a fixed cost, in the latter each *ingredient* has a fixed cost.

We want to minimise the total cost of all our meals while obeying customer needs for variety.

### Complication 4: Good Meals

This feels like an area that might benefit from AI / ML.

Assign a variable to our meals that we want to maximise i.e. happiness.

### Complication 5: Modelling Real Consumption

This feels like an area that might benefit from AI / ML.

Model the real consumption of meals with various sub-complications:
* There are fixed portions of a meal
* People eat some amount of the meals each day (this might be predictable, or more likely partly predictable)
* Meals last only a certain amount of time before they need to be disposed of and this varies by type of meal.