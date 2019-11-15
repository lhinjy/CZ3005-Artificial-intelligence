append([], Y, Y).
append([H|X], Y, [H|Z]) :- append(X, Y, Z).

meal_healthy(healthy).
meal_value(value).
meal_vegan(vegan).
meal_veggie(veggie).

meals([normal, healthy, value, vegan, veggie]).
breads([italian_wheat, hearty_italian, honey_oat, multigrain, flatbread]).
meats([chicken_teriyaki, cold_cut_trio, meatball_marinara_melt, roast_beef, subway_club]).
veggies([cucumbers, lettuce, tomatoes, pickles]).
fatty_sauces([mayonnaise,ranch, bbq]).
non_fatty_sauces([honey_mustard, sweet_onion]).
cheese_topups([processed_cheddar, monterey_cheddar]).
non_cheese_topups([avocado, tuna]).
sides([chips, cookie, drink]).

ask_meals(X) :- meals(L), member(X,L).

ask_breads(X) :- breads(L), member(X,L).

ask_mt(X) :- findall(X, (meal_chosen(Y), \+meal_vegan(Y), \+meal_veggie(Y), meats(X)), X).
ask_meat(X) :- ask_mt(L) , member(X,L).
ask_meats(X) :- ask_meat(L) , member(X,L).

ask_veggies(X) :- veggies(L), member(X,L).

ask_ss(X) :- findall(X, (meal_chosen(Y), meal_healthy(Y) -> non_fatty_sauces(X);
                 fatty_sauces(L1), non_fatty_sauces(L2), append(L1, L2, X)), X).
ask_sauce(X) :- ask_ss(L), member(X,L).
ask_sauces(X) :- ask_sauce(L), member(X,L).

ask_ts(X) :- findall(X, (meal_chosen(Y), \+meal_value(Y) -> (meal_vegan(Y) -> non_cheese_topups(X);
                 cheese_topups(L1), non_cheese_topups(L2), append(L1, L2, X))), X).
ask_topup(X) :- ask_ts(L), member(X,L).
ask_topups(X) :- ask_topup(L), member(X,L).

ask_sides(X) :- sides(L), member(X,L).

show_meals(Meals) :- findall(X, meal_chosen(X), Meals).
show_breads(Breads) :- findall(X, bread_chosen(X), Breads).
show_meats(Meats) :- findall(X, meat_chosen(X), Meats).
show_veggies(Veggies) :- findall(X, veggie_chosen(X), Veggies).
show_sauces(Sauces) :- findall(X, sauce_chosen(X), Sauces).
show_topups(TopUps) :- findall(X, topup_chosen(X), TopUps).
show_sides(Sides) :- findall(X, side_chosen(X), Sides).