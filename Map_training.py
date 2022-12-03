
# let's keep praticiing all of the python functions until we get used
# Maps functions

# First we r gonna create a list:

Dic = [('Brunch', 60), ('Coffee', 15), ('Hotel', 418), ('Airplane', 400)]

# Now lez create a function that converts CAD to USD

Func = lambda x: (x[0], (x[1]*1.38))

print(list(map(Func, Dic)))


