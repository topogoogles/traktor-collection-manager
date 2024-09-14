import TraktorBuddy

collection = TraktorBuddy.Collection()

for track in collection.tracks():
    print(track.key())


# Creates a list of attributes from a track object of the collection.track()
track_properties = []

for property in dir(collection.tracks()[500]):
    track_properties.append(property)

print(track_properties)


# Returns a list of names of all callable attributes that don't start with "set"
def get_methods(obj):
    return [
        name
        for name in dir(obj)
        if callable(getattr(obj, name)) and not name.startswith("set")
    ]


methods = get_methods(collection.tracks()[500])

print(methods)
