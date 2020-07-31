import copy
from itunes import iTunesEntryReader
import time


def subset_main(data_set, target):
    """
        Assumes Data_set is a valid list
        main function works for both any ints and itunes object reader

        The itunes.py already had itunesEntry with the "+" operand already overridden
    """
    # provide a special test to dispose targets larger than the sum of all elements in the master set.
    if sum(data_set) < target:
        raise ValueError("Target is greater than largest sum")

    choices = []
    current_max = Sublist()

    # loop through data_set
    for i in range(len(data_set)):
        entry = data_set[i]

        # if list is empty create a sublist with data_set passed then append to choices
        if not choices:
            sub = Sublist(data_set)
            choices.append(sub)
        # create a copy so the list doesnt expand while looping
        choices_copy = [sublist for sublist in choices]
        for sublist in choices_copy:
            sublist_copy = sublist.add_item(i)
            if sublist_copy.sum <= target:
                choices.append(sublist_copy)
                current_max = max(current_max, sublist_copy, key=lambda x: x.sum)
            if sublist_copy.sum == target:
                current_max = max(current_max, sublist_copy, key=lambda x: x.sum)
                return current_max

    return current_max


class Sublist:
    def __init__(self, original_objects=None):
        self._original_objects = original_objects
        self._sum = 0
        self._indices = []

    def __str__(self):
        ret_str = "Sublist ----------------------------- \n"
        ret_str += "  sum: " + str(self._sum) + "\n"
        num_indices = len(self._indices)
        for k in range(num_indices):
            ret_str += "  item[" + str(self._indices[k]) + \
                "] = " + str(self._original_objects[self._indices[k]])
        ret_str += "\n"
        return ret_str

    @property
    def sum(self):
        return self._sum

    def add_item(self, index_of_item_to_add):
        # To Do
        new_sublist = self._dc()
        new_sublist._indices += [index_of_item_to_add]
        new_sublist._sum += self._original_objects[index_of_item_to_add]
        return new_sublist

    def _dc(self):
        # To Do (copy method)
        sum_copy = copy.deepcopy(self._sum)
        indicies_copy = copy.deepcopy(self._indices)
        list = Sublist(self._original_objects)
        list._indices = indicies_copy
        list._sum = sum_copy
        return list

    def __repr__(self):
        return str(self.sum)


if __name__ == "__main__":
    itunes_data_set = iTunesEntryReader("itunes_file.txt")
    itunes_target = 3600

    print("Itunes subset sum: ")
    t1 = time.time()
    max_sublist = subset_main(itunes_data_set, itunes_target)
    t2 = time.time()
    print(str(max_sublist))
    print('runtime: ', t2 - t1)
    print(" =========================================== ")

    # regular int print
    import random
    data_set = [random.randint(200, 500) for _ in range(80)]
    target_list = [100, 182, 200, 500, 3600, 5000]
    target = 3600

    print('Main with any ints')
    print(str(subset_main(data_set, target)))
    print('target sum: ', target)
    for target in target_list:
        try:
            t1 = time.time()
            max_sl = subset_main(data_set, target)
            t2 = time.time()
            print(str(max_sl))
            print('runtime: ', t2 - t1)
        except ValueError as err:
            print(err)

    print(str(subset_main(([20, 12, 22, 15, 25, 19, 29, 18, 11, 13, 17]), 200)))

    ''' 
        Itunes subset sum: 
        Sublist ----------------------------- 
          sum: 3600
          item[0] = Carrie Underwood -> Cowboy Casanova: 3:56  item[1] = Carrie Underwood -> Quitter: 3:40  item[2] = Rihanna -> Russian Roulette: 3:48  item[4] = Foo Fighters -> Monkey Wrench: 3:50  item[5] = Eric Clapton -> Pretending: 4:43  item[6] = Eric Clapton -> Bad Love: 5:08  item[7] = Howlin' Wolf -> Everybody's In The Mood: 2:58  item[8] = Howlin' Wolf -> Well That's All Right: 2:55  item[9] = Reverend Gary Davis -> Samson and Delilah: 3:36  item[11] = Roy Buchanan -> Hot Cha: 3:28  item[12] = Roy Buchanan -> Green Onions: 7:23  item[13] = Janiva Magness -> I'm Just a Prisoner: 3:50  item[14] = Janiva Magness -> You Were Never Mine: 4:36  item[15] = John Lee Hooker -> Hobo Blues: 3:07  item[16] = John Lee Hooker -> I Can't Quit You Baby: 3:02
        
        runtime:  1.7019579410552979
         =========================================== 
        Main with any ints
        Sublist ----------------------------- 
          sum: 3600
          item[1] = 323  item[2] = 400  item[3] = 438  item[4] = 274  item[5] = 349  item[6] = 267  item[7] = 425  item[8] = 299  item[9] = 404  item[12] = 421
        
        target sum:  3600
        Sublist ----------------------------- 
          sum: 0
        
        
        runtime:  0.0004119873046875
        Sublist ----------------------------- 
          sum: 0
        
        
        runtime:  0.0004558563232421875
        Sublist ----------------------------- 
          sum: 200
          item[44] = 200
        
        runtime:  0.00022983551025390625
        Sublist ----------------------------- 
          sum: 500
          item[6] = 267  item[19] = 233
        
        runtime:  0.0013251304626464844
        Sublist ----------------------------- 
          sum: 3600
          item[1] = 323  item[2] = 400  item[3] = 438  item[4] = 274  item[5] = 349  item[6] = 267  item[7] = 425  item[8] = 299  item[9] = 404  item[12] = 421
        
        runtime:  0.05302762985229492
        Sublist ----------------------------- 
          sum: 5000
          item[0] = 239  item[1] = 323  item[2] = 400  item[4] = 274  item[7] = 425  item[8] = 299  item[9] = 404  item[10] = 436  item[11] = 294  item[12] = 421  item[13] = 456  item[14] = 268  item[15] = 433  item[16] = 328
        
        runtime:  1.476395845413208
        Sublist ----------------------------- 
          sum: 190
          item[0] = 20  item[1] = 12  item[2] = 22  item[3] = 15  item[4] = 25  item[5] = 19  item[6] = 29  item[7] = 18  item[9] = 13  item[10] = 17

    '''



