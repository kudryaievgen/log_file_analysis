import json
import datetime

PRODUCT_VERSION_PATTERN = "Product version:"


def parse_log_file(in_file_path, expected_version, out_file_path, log_level, start_date, end_date):
    with open(in_file_path, "r") as file:
        #version_line = file.readline()
        #cur_version = get_version(version_line)

        #if cur_version != expected_version:
         #   raise Exception("Invalid version: {number}".format(number=cur_version))

        result_records = []
        from_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        for line in file:
            try:
                str_date = line.split(' ')[0]
                str_time = line.split(' ')[1]
                year = int(str_date.split('-')[0])
                mounth = int(str_date.split('-')[1])
                day = int(str_date.split('-')[2])
                hour = int(str_time.split(':')[0])
                minute = int(str_time.split(':')[1])
                second = str_time.split(':')[2]
                sec = int(second.split(',')[0])
                date_from_log = datetime.datetime(year, mounth, day, hour, minute, sec)
                if from_date < date_from_log < to_date:
                    if line.split(' ')[2] in log_level:
                        result_records.append(line)
            except:
                result_records.append(line)

        if result_records:
            with open(out_file_path, "w") as out_file:
                out_file.writelines(result_records)

            print("Result records saved.")


def get_version(version_str):
    if version_str.startswith(PRODUCT_VERSION_PATTERN):
        version_number = version_str[len(PRODUCT_VERSION_PATTERN):]
        return version_number.strip()
    else:
        raise Exception("Invalid file format, version is missing")


if __name__ == "__main__":
    with open('config.json', 'r') as file:
        config = json.load(file)
        try:
            parse_log_file(in_file_path=config['in'],
                           expected_version=config['version'],
                           out_file_path=config['out'],
                           log_level=config['level'],
                           start_date=config['from'],
                           end_date=config['to'])
        except IOError as e:
            print(str(e))
        except Exception as e:
            print(str(e))
