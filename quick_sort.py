import random
from tabulate import tabulate
import time
import copy



def median_three(list_to_sort, left, right):
    center = (left + right) // 2
    if list_to_sort[center] < list_to_sort[left]:
        list_to_sort[left], list_to_sort[center] = \
            list_to_sort[center], list_to_sort[left]

    if list_to_sort[right] < list_to_sort[left]:
        list_to_sort[left], list_to_sort[right] = \
            list_to_sort[right], list_to_sort[left]

    if list_to_sort[right] < list_to_sort[center]:
        list_to_sort[center], list_to_sort[right] = \
            list_to_sort[right], list_to_sort[center]

    list_to_sort[center], list_to_sort[right - 1] = \
        list_to_sort[right - 1], list_to_sort[center]

    return list_to_sort[right - 1]


def quick_sort_x(list_to_sort, recursion_limit):
    if recursion_limit < 2:
        raise ValueError

    _quick_sort(list_to_sort, 0, len(list_to_sort) - 1, recursion_limit)

def _quick_sort(list_to_sort, left, right, recursion_limit):

    if left + recursion_limit <= right:
        pivot = median_three(list_to_sort, left, right)
        i = left
        j = right - 1
        while i < j:
            for i in range(i + 1, j + 1):
                if pivot <= list_to_sort[i]:
                    break
            for j in range(j - 1, i - 1, -1):
                if list_to_sort[j] <= pivot:
                    break
            if i < j:
                list_to_sort[i], list_to_sort[j] = \
                    list_to_sort[j], list_to_sort[i]
            else:
                break

        list_to_sort[i], list_to_sort[right - 1] = \
            list_to_sort[right - 1], list_to_sort[i]

        _quick_sort(list_to_sort, left, i - 1, recursion_limit)
        _quick_sort(list_to_sort, i + 1, right, recursion_limit)

    else:
        insertion_sort(list_to_sort, left, right)

def insertion_sort(target, left, right):

    for pos in range(left + 1, right + 1):
        tmp = target[pos]
        k = pos
        while tmp < target[k - 1] and k > 0:
            target[k] = target[k - 1]
            k -= 1
        target[k] = tmp


if __name__ == "__main__":
    list_sizes = [40000, 80000, 160000, 320000]
    results = {"Recursion Limit": [str(i) for i in range(300, 0, -2)]}

    # loop through list size
    for list_size in list_sizes:
        unsorted_list = [random.randint(0, list_size) for _ in range(list_size)]

        # for results table
        if list_size not in results:
            results[list_size] = []

        for recursion_limit in range(300, 0, -2):
            unsorted_list_copy = copy.deepcopy(unsorted_list)
            # verbosity for sanity reasons
            print(f"WHERE IN LOOP?: {list_size} {recursion_limit}")

            start = time.perf_counter()

            quick_sort_x(unsorted_list_copy, recursion_limit)

            stop = time.perf_counter()
            elapsed_time = stop - start

            results[list_size].append(elapsed_time)

    print(tabulate(results, headers='keys'))


"""
 Recursion Limit     40000     80000    160000    320000
-----------------  --------  --------  --------  --------
              300  0.634548  1.24788   2.56264    5.30451
              298  0.624793  1.24017   2.54155    5.34273
              296  0.610134  1.23984   2.51482    5.28355
              294  0.607037  1.22844   2.5361     5.24439
              292  0.596828  1.23289   2.51251    5.23615
              290  0.592649  1.22907   2.48829    5.23985
              288  0.589261  1.20917   2.47464    5.19155
              286  0.584014  1.19488   2.49008    5.09548
              284  0.580177  1.18102   2.47425    5.10108
              282  0.577764  1.17168   2.44563    5.07538
              280  0.574443  1.17423   2.44202    5.07342
              278  0.579001  1.17509   2.46703    5.01255
              276  0.576897  1.19517   2.42466    5.07146
              274  0.570885  1.17898   2.3934     4.97761
              272  0.561216  1.15992   2.39464    4.96056
              270  0.555121  1.15765   2.40907    4.92339
              268  0.553056  1.15272   2.41443    4.89641
              266  0.580067  1.13633   2.38351    4.88906
              264  0.55334   1.12055   2.34436    4.86047
              262  0.547139  1.12108   2.33627    4.78067
              260  0.548639  1.12919   2.3259     4.77077
              258  0.547516  1.11557   2.2949     4.72098
              256  0.539628  1.12529   2.27385    4.70683
              254  0.541947  1.11296   2.29221    4.65943
              252  0.546878  1.10688   2.2809     4.70411
              250  0.528499  1.10079   2.25694    4.82797
              248  0.531735  1.09827   2.23545    4.62032
              246  0.518493  1.09024   2.23059    4.51473
              244  0.51423   1.08535   2.22227    4.5893
              242  0.514683  1.084     2.19998    4.76362
              240  0.51268   1.06794   2.17157    4.53943
              238  0.507709  1.05859   2.15912    4.55581
              236  0.504476  1.07259   2.18209    4.49946
              234  0.496346  1.06061   2.13961    4.52323
              232  0.495928  1.05324   2.11324    4.33642
              230  0.487351  1.04164   2.10677    4.40292
              228  0.482811  1.0311    2.11733    4.37339
              226  0.483029  1.0316    2.10065    4.30551
              224  0.47706   1.03074   2.07151    4.25049
              222  0.470197  1.01679   2.05876    4.2429
              220  0.4667    1.02328   2.04806    4.18928
              218  0.468898  0.992158  2.05042    4.15578
              216  0.464355  0.988425  2.07047    4.15694
              214  0.46079   0.978516  2.03326    4.12577
              212  0.459526  0.968614  1.99603    4.09165
              210  0.469391  0.955524  1.99556    4.12734
              208  0.456454  0.94296   1.9687     4.05714
              206  0.455594  0.943386  1.99164    4.03927
              204  0.46392   0.949359  1.94417    4.18191
              202  0.451477  0.9456    1.91813    4.0278
              200  0.446198  0.928138  1.92909    3.98012
              198  0.449661  0.921042  1.92602    3.97826
              196  0.445533  0.915404  1.92455    3.91549
              194  0.437401  0.909294  1.88057    3.87231
              192  0.446726  0.894947  1.87811    3.84276
              190  0.436292  0.885034  1.86636    3.92136
              188  0.437086  0.882826  1.8549     3.80253
              186  0.436379  0.87289   1.82582    4.2045
              184  0.431617  0.870074  1.81365    3.97553
              182  0.427843  0.881223  1.80034    3.91596
              180  0.421901  0.86575   1.8076     3.98437
              178  0.421299  0.85512   1.79161    4.18132
              176  0.416556  0.841792  1.76814    4.95314
              174  0.409512  0.838397  1.73947    6.06496
              172  0.411635  0.826513  1.74117    4.35205
              170  0.409994  0.820212  1.73142    5.33826
              168  0.399057  0.817325  1.7191     4.95349
              166  0.399718  0.808511  1.69929    4.6989
              164  0.394386  0.801933  1.67855    4.69946
              162  0.389261  0.793509  1.65707    4.47158
              160  0.388801  0.807251  1.66215    4.33687
              158  0.394546  0.784703  1.64244    3.99199
              156  0.390781  0.786607  1.64819    3.58073
              154  0.381494  0.776546  1.65859    3.47562
              152  0.379017  0.777181  1.62678    3.46992
              150  0.372356  0.763342  1.61578    3.41238
              148  0.369346  0.756651  1.58384    3.45278
              146  0.376417  0.753309  1.56925    3.74072
              144  0.364519  0.75144   1.55386    3.37768
              142  0.357818  0.740362  1.5714     3.34182
              140  0.353947  0.73573   1.53904    3.3089
              138  0.351343  0.728183  1.52011    3.22004
              136  0.349989  0.740214  1.51149    3.22258
              134  0.346246  0.724164  1.50184    3.19785
              132  0.342764  0.718255  1.51551    3.16789
              130  0.341368  0.714629  1.47869    3.13812
              128  0.336206  0.705237  1.45714    3.15714
              126  0.334749  0.69421   1.444      3.08968
              124  0.330908  0.691567  1.43502    3.05086
              122  0.324292  0.681827  1.45499    3.47521
              120  0.323632  0.675357  1.44197    3.06007
              118  0.320992  0.670416  1.42549    2.99072
              116  0.320228  0.666288  1.40845    3.00607
              114  0.312494  0.663063  1.39081    3.41713
              112  0.313393  0.660646  1.38342    3.03787
              110  0.31417   0.649338  1.37105    2.93436
              108  0.305919  0.65346   1.37051    2.88041
              106  0.313332  0.65021   1.36964    2.85121
              104  0.307134  0.636008  1.34831    2.85389
              102  0.300119  0.628378  1.34688    2.80633
              100  0.304165  0.641021  1.31672    2.79868
               98  0.307113  0.652695  1.30324    2.75861
               96  0.298984  0.611336  1.29709    2.76798
               94  0.289806  0.614178  1.28107    2.77541
               92  0.28953   0.59411   1.28444    2.71146
               90  0.286136  0.595436  1.25815    2.72597
               88  0.279641  0.5917    1.25621    2.65605
               86  0.277159  0.588694  1.23327    2.61562
               84  0.279633  0.574433  1.21899    2.68555
               82  0.27471   0.571657  1.23155    2.64073
               80  0.271938  0.563252  1.21157    2.58508
               78  0.273461  0.572202  1.21106    2.53903
               76  0.26664   0.557834  1.18457    2.57038
               74  0.263026  0.562863  1.17757    2.53173
               72  0.259017  0.562916  1.18027    2.48549
               70  0.254092  0.546612  1.1657     2.49786
               68  0.258456  0.539239  1.1491     2.514
               66  0.250545  0.529544  1.13777    2.43161
               64  0.249385  0.533496  1.12766    2.51855
               62  0.245346  0.521071  1.12605    2.57003
               60  0.241988  0.514109  1.10802    2.48978
               58  0.239064  0.525738  1.08635    2.32612
               56  0.236094  0.510259  1.10118    2.46093
               54  0.234967  0.497533  1.07804    2.35679
               52  0.230591  0.489056  1.05297    2.2955
               50  0.229553  0.486672  1.04301    2.2688
               48  0.228152  0.479465  1.03241    2.26323
               46  0.223336  0.472125  1.02959    2.2122
               44  0.223408  0.479915  1.03428    2.22743
               42  0.219403  0.466806  1.01235    2.1811
               40  0.216493  0.462281  1.00077    2.16774
               38  0.214806  0.456905  0.984703   2.16478
               36  0.225975  0.468451  0.979821   2.16782
               34  0.212541  0.453102  0.96418    2.18023
               32  0.211378  0.444699  0.959927   2.10479
               30  0.223037  0.44443   0.958164   2.07647
               28  0.209582  0.448251  0.955591   2.11361
               26  0.214996  0.435682  0.946455   2.06203
               24  0.204395  0.435946  0.946986   2.05235
               22  0.203829  0.430218  0.935407   2.03541
               20  0.203078  0.425635  0.943591   2.0401
               18  0.200314  0.425128  0.924026   2.02727
               16  0.200628  0.424405  0.924157   2.03198
               14  0.199659  0.423693  0.919215   2.01383
               12  0.199828  0.422717  0.917642   2.00542
               10  0.200253  0.428558  0.929153   2.03246
                8  0.211384  0.429645  0.948602   2.0145
                6  0.206932  0.440288  0.954289   2.20517
                4  0.212699  0.450397  0.987371   2.7321
                2  0.22649   0.489392  1.04065    2.53871


Overall, the algorithm is very fast compared to some other sort algorithm such as insertion sort (on its own) 
and the table really shows how the algorithm is O(n log(n)).. as the recursion limits go up, the time of the 
algorithm follows suit but at a rate much slower than O(n) and really follows the shape of O(n log(n)). 

By looking at the table, it looks like that the most optimal recursion limit is somewhere 
between 50 - 10 the times around these recursion limits are fairly similar; below 10 is also a bit slower.
However, since the time complexity is O(n log(n)) it still looks like a very fast sorting algorithm regardless. 
"""