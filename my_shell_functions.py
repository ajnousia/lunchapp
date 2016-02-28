import pickle

def save_entity_object_to_disk(entity_object):
    with open("old_entity.pkl", "wb") as output:
        pickle.dump(entity_object, output, -1)

def print_test():
    print "hello"
