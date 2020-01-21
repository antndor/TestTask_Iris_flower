import io 
import csv
import numpy as np

from numpy import inf

from tabulate import tabulate


#  Metrics

def in_interval(from_, to):
    def wrap(list_):
        total_count = len(list_)
        cut_count = len([el for el in list_ if from_ <= el < to])
        percent = float(cut_count) / total_count * 100

        return cut_count,  percent

    return wrap

# Main

def read_data(file_path):
    total_flowers = {
        'lengths': [],
        'widths': []
    }

    flowers = {}

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for rows in reader:
            length = float(rows[0])
            width = float(rows[1])
            name = rows[4]

            total_flowers['lengths'].append(length)
            total_flowers['widths'].append(width)

            if name not in flowers:
                flowers[name] = {
                    'lengths': [length],
                    'widths': [width]
                }
            else:
                flowers[name]['lengths'].append(length)
                flowers[name]['widths'].append(width)
                
        flowers['Total'] = total_flowers

    return flowers
  

def calculate_metrics(flowers):
    metrics = {}
    
    functions = [
        (len, int, 'N', []),
        (np.mean, u'\u2063{0:.2f}'.format, 'MEAN', []),
        (min, u'\u2063{0:.1f}'.format, 'MIN', []),
        (np.median, u'\u2063{0:.2f}'.format, 'MEDIAN', []),
        (max, u'\u2063{0:.1f}'.format, 'MAX', []),
        (np.std, u'\u2063{0:.2f}'.format, 'ST.DEV', []),
        (in_interval(-inf, 5),
         lambda e: '{} ( {:.1f})'.format(*e),
         '< 5',
         ['lengths']),
        (in_interval(5, 6),
         lambda e: '{} ( {:.1f})'.format(*e),
         '>= 5 AND < 6',
         ['lengths']),
        (in_interval(6, 7),
         lambda e: '{} ( {:.1f})'.format(*e),
         '>= 6 AND < 7',
         ['lengths']),
        (in_interval(7, inf),
         lambda e: '{} ( {:.1f})'.format(*e),
         '>= 7',
         ['lengths']),
        (in_interval(-inf, 3),
         lambda e: '{} ( {:.1f})'.format(*e),
         '< 3',
         ['widths']),
        (in_interval(3, 3.5),
         lambda e: '{} ( {:.1f})'.format(*e),
         '>= 3 and < 3.5',
         ['widths']),
        (in_interval(3.5, 4),
         lambda e: '{} ( {:.1f})'.format(*e),
         '>= 3.5 AND < 4',
         ['widths']),
    ]

    for funcs in functions:
        func_metric = funcs[0]
        func_view = funcs[1]
        name = funcs[2]
        accepted_params = funcs[3]

        flowers_metrics = {}

        for flower_name, flower_data in flowers.items():
            data = {}
            for param in ['lengths', 'widths']:
                if not accepted_params or param in accepted_params:
                    data[param[:-1]] = func_view(func_metric(flower_data[param]))
    
            flowers_metrics[flower_name] = data

        metrics[name] = flowers_metrics

    return metrics      


def print_table(flower_names, metrics):
    headers = [''] + flower_names
    
    table_cm_length = []
    table_percent_length = []
    table_cm_width = []
    table_percent_width = []

    for metric, data in metrics.items():
        is_percent = '<' in metric or '>' in metric
        row_length = []
        row_width = []
        row_percent = {
            'length': [],
            'width': []
        }

        for flower_name in flower_names:
            if is_percent:
                key = list(data[flower_name].keys())[0]
                row_percent[key].append(data[flower_name][key])
            else:
                row_length.append(data[flower_name]['length'])
                row_width.append(data[flower_name]['width'])
        
        if row_percent['length']:
            table_percent_length.append([metric] + row_percent['length'])
        if row_percent['width']:
            table_percent_width.append([metric] + row_percent['width'])
        if row_length:
            table_cm_length.append([metric] + row_length)
        if row_width:
            table_cm_width.append([metric] + row_width)

    table = []
    table.append(['SEPAL LENGTH [CM]'])
    table.extend(table_cm_length)

    table.append([])
    table.append(['SEPAL LENGTH (%)'])
    table.extend(table_percent_length)

    table.append([])
    table.append(['SEPAL WIDTS [CM]'])
    table.extend(table_cm_width)

    table.append([])
    table.append(['SEPAL WIDTS (%)'])
    table.extend(table_percent_width)
    
    with io.open('iris-flowers.txt', 'w', encoding='utf8') as f:
        data = tabulate(table, headers=headers)
        f.write(data)


if __name__ == '__main__':
    file_path = 'iris.data'

    flowers = read_data(file_path)
    metrics = calculate_metrics(flowers)

    flower_names = list(flowers.keys())
    print_table(flower_names, metrics)

