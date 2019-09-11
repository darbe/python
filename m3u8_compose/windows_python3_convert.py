import os
import clean_name

result_file = []
suffix = ".txt"

def all_path(dirname):
    result = []
    if not os.path.isdir(dirname):
        return
    for filename in os.listdir(dirname):
        if os.path.exists(filename) and os.path.isfile(filename):
            apath = os.path.join(dirname, filename)
            result.append(apath)
    return result

def compose_video(file_path):
    result_file =  all_path(file_path)
    for cur_file_all_name in result_file:
        if not cur_file_all_name.endswith(".m3u8"):
            continue
        (cur_file_path, temp_file_name) = os.path.split(cur_file_all_name)
        (file_name, extension) = os.path.splitext(temp_file_name)
        file_name_out_complete = clean_name.clean_file_name(file_name) + ".mp4"
        file_name_in_complete = temp_file_name
        file_name_in_complete_new = clean_name.clean_file_name(file_name) +  suffix
        f = open(file_name_in_complete,  mode = 'r', encoding='UTF-8')
        f_new = open(file_name_in_complete_new, mode='w', encoding='UTF-8')
        cur_dir_name = ""
        for line in f:
            if "file:///storage/emulated/0/QQBrowser/" in line:
                index = line.rfind("/")
                trunct_line = line[0:index]
                dir_index = trunct_line.rfind("/")
                cur_dir_name = trunct_line[dir_index+2:]
                if os.path.exists(cur_dir_name) and os.path.isdir(cur_dir_name):
                    break
                else :
                    print("Error not exist dir", cur_dir_name,cur_file_name)
                    return
        f.close()
        f = open(file_name_in_complete,  mode = 'r', encoding='UTF-8')
        for line in f:
            if "file:///storage/emulated/0/QQBrowser/" in line:
                index = line.rfind("/")
                index2 = line.find("file")
                pre = line[:index2]
                end = line[index+1:]
                line = pre + file_path + "\\" + cur_dir_name + "\\" + end
            f_new.write(line)
        f.close()
        f_new.close()
        cmd = """ffmpeg -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i """ + file_name_in_complete_new + """  -c copy """ + file_name_out_complete
        os.system(cmd)
        print("process " , file_name_in_complete, " to ", file_name_out_complete , "done ...")
        os.remove(file_name_in_complete_new)
compose_video("C:\\Users\\dabin\\Downloads\\video")
            
