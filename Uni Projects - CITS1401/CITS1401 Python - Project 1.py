
# Program to test whether simpler methods can yield similar result
# when countries are ranked by Life Ladder score in descending order

import os


# Ask user to input the name of the file, metric and method to work on
def input_info():
    fname = input("Please enter the file name to open: ")
    if not os.path.isfile(fname):
        print(fname + " does not exist")
        return None

    Metric = str(
        input("Please choose the metric to be used (choose from minimum, mean, median and harmonic mean): ")).lower()
    if Metric not in ("minimum", "mean", "median", "harmonic mean"):
        print("The enter is not from the options")
        return None

    Action = str(input("Please choose the action to be taken (list and correlation): ")).lower()
    if Action not in ("list", "correlation"):
        print("The enter is not from the options")
        return None

    return fname, Metric, Action


# Get the sequence of words from the file, replace missing data with none, output country_data
def read_file(Input_info):
    fname = Input_info[0]
    infile = open(fname, "r")
    country_data = [line.strip().split(",") for line in infile][1:]

    for i in range(len(country_data)):
        lst = country_data[i]
        for j in range(len(lst)):
            if j < 1:
                lst[j] = lst[j]
            else:
                if lst[j] == "":
                    lst[j] = None
                else:
                    lst[j] = float(lst[j])
    return country_data


# Get minimum and maximum values for each row
def min_max(country_data):
    Log_GDP = []
    Soci_supp = []
    Life_expec = []
    Free_choice = []
    Generosity = []
    Confi = []

    for i in range(len(country_data)):
        Log_GDP.append(country_data[i][2])
        Soci_supp.append(country_data[i][3])
        Life_expec.append(country_data[i][4])
        Free_choice.append(country_data[i][5])
        Generosity.append(country_data[i][6])
        Confi.append(country_data[i][7])

    Log_mm = (min(filter(None, Log_GDP)), max(filter(None, Log_GDP)))
    Soci_mm = (min(filter(None, Soci_supp)), max(filter(None, Soci_supp)))
    Life_mm = (min(filter(None, Life_expec)), max(filter(None, Life_expec)))
    Free_mm = (min(filter(None, Free_choice)), max(filter(None, Free_choice)))
    Gen_mm = (min(filter(None, Generosity)), max(filter(None, Generosity)))
    Confi_mm = (min(filter(None, Confi)), max(filter(None, Confi)))

    return [Log_mm, Soci_mm, Life_mm, Free_mm, Gen_mm, Confi_mm]


# Normalize the data using formula: (score - min)/(max-min), output New_country_data
def normalize(Min_max, country_data):
    Log_mm = Min_max[0]
    Soci_mm = Min_max[1]
    Life_mm = Min_max[2]
    Free_mm = Min_max[3]
    Gen_mm = Min_max[4]
    Confi_mm = Min_max[5]
    New_country_data = []

    # Nomalize data
    for i in range(len(country_data)):
        lst = country_data[i]
        for j in range(2, len(lst)):
            if lst[j] is not None:
                if j == 2:
                    lst[2] = abs(lst[2] - Log_mm[0]) / (Log_mm[1] - Log_mm[0])
                elif j == 3:
                    lst[3] = abs(lst[3] - Soci_mm[0]) / (Soci_mm[1] - Soci_mm[0])
                elif j == 4:
                    lst[4] = abs(lst[4] - Life_mm[0]) / (Life_mm[1] - Life_mm[0])
                elif j == 5:
                    lst[5] = abs(lst[5] - Free_mm[0]) / (Free_mm[1] - Free_mm[0])
                elif j == 6:
                    lst[6] = abs(lst[6] - Gen_mm[0]) / (Gen_mm[1] - Gen_mm[0])
                elif j == 7:
                    lst[7] = abs(lst[7] - Confi_mm[0]) / (Confi_mm[1] - Confi_mm[0])
            else:
                lst[j] = None

        # To remove None from the metrics and create a new list
        y = [x for x in lst if x is not None]
        New_country_data.append(y)

    return New_country_data


# Compute the nominated metric using the normalised values
def metrics(New_country_data):
    metric_min = []
    metric_mean = []
    metric_median = []
    metric_h_mean = []
    study_rank = []

    for i in range(len(New_country_data)):
        x = sorted(New_country_data[i][2:])
        lst = New_country_data[i][:2] + x

        # Compute minimum and mean metric
        metric_min.append([min(lst[2:]), lst[0]])
        metric_mean.append([sum(lst[2:]) / len(lst[2:]), lst[0]])

        # Compute Life Ladder list for later reference
        study_rank.append([lst[1], lst[0]])

        # Compute median metric
        mid = len(x) // 2
        median = (x[mid] + x[~mid]) / 2
        metric_median.append([median, lst[0]])

        # Compute harmonic mean metric(avoid Zeros), if the sum of values equals to zero: print error
        new_list = []
        for ele in lst:
            if ele != float(0):
                new_list.append(ele)

        if sum(1. / ele for ele in new_list[2:]) != float(0):
            metric_h_mean.append([len(new_list[2:]) / sum(1. / ele for ele in new_list[2:]), new_list[0]])
        else:
            print(new_list[0] + " : Error! Harmonic mean cannot be produced due to zero.")

    # Sort the metircs by descending order
    metric_min.sort(reverse=True)
    metric_mean.sort(reverse=True)
    metric_median.sort(reverse=True)
    metric_h_mean.sort(reverse=True)
    study_rank.sort(reverse=True)

    return metric_min, metric_mean, metric_median, metric_h_mean, study_rank


# Use user's input to compute and print the outcome
def action_M(Norm, Input_info):
    metric = Input_info[1]
    action = Input_info[2]

    minimum, mean, median, h_mean = "minimum", "mean", "median", "harmonic mean"
    action1, action2 = "list", "correlation"

    # If list
    if action == action1:
        print("\nRanked list of countries' happiness scores based on the " + metric + " metric is:\n")
        if metric == minimum:
            for item in Norm[0]:
                print(item[1], round(item[0], 4))
        if metric == mean:
            for item in Norm[1]:
                print(item[1], round(item[0], 4))
        if metric == median:
            for item in Norm[2]:
                print(item[1], round(item[0], 4))
        if metric == h_mean:
            for item in Norm[3]:
                print(item[1], round(item[0], 4))

    # If correlation
    if action == action2:
        print(
            "\nThe correlation coefficient between the study ranking and the ranking using the  " + metric + " metric is: ",
            end="")
        if metric == minimum:
            Cor = Rho(Norm[4], Norm[0])
            print(round(Cor, 4))
        if metric == mean:
            Cor = Rho(Norm[4], Norm[1])
            print(round(Cor, 4))
        if metric == median:
            Cor = Rho(Norm[4], Norm[2])
            print(round(Cor, 4))
        if metric == h_mean:
            Cor = Rho(Norm[4], Norm[3])
            print(round(Cor, 4))


# Compute correlation coefficent
def Rho(a, b):
    list_study = a
    list_metric = b

    rank_diff = 0
    N = len(list_study)

    for i in range(len(list_study)):
        country = list_study[i][1]
        for j in range(len(list_metric)):
            if list_metric[j][1] == country:
                d = i - j
                break
        rank_diff += d * d
        r = 1 - 6 * rank_diff / (N * (N * N - 1))

    return (r)


def main():
    Input_info = input_info()
    if Input_info is None:
        print("Program stopped because of the wrong input")
        return None
    country_data = read_file(Input_info)
    Min_max = min_max(country_data)
    New_country_data = normalize(Min_max, country_data)
    Norm = metrics(New_country_data)
    action_M(Norm, Input_info)
    Rho(Norm, Norm)


main()