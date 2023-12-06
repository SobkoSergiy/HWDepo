import time
import pathlib 
from threading import Thread  
import logging            


suffix_dict = {
    'JPEG': 'images', 'PNG': 'images', 'JPG': 'images', 'SVG': 'images', 'BMP': 'images',
    'AVI': 'video', 'MP4': 'video', 'MOV': 'video', 'MKV': 'video',
    'DOC': 'documents', 'DOCX': 'documents', 'TXT': 'documents', 'PDF': 'documents', 
    'XLS': 'documents', 'XLSX': 'documents', 'PPTX': 'documents', 
    'MP3': 'audio', 'OGG': 'audio', 'WAV': 'audio', 'AMR': 'audio',
    'ZIP': 'archives', 'GZ': 'archives', 'TAR': 'archives',
}
files_dict = {'images': [], 'video': [], 'documents': [], 'audio': [], 'archives': [], 'unknown': []}
known_suffix = set()
unknown_suffix = set()
folders_list = []


# same function for synchronous and threads
def select_file(path):  # fill files_dict() depending on category of file suffix
    suf = path.suffix[1:].upper()
    categ = suffix_dict.get(suf)    
    if categ:
        files_dict[categ].append(path)
        known_suffix.add(suf)
    else:
        files_dict['unknown'].append(path)
        unknown_suffix.add(suf)

def view_folder(path):  # view & preparing files & folders to further processing
    for file in path.iterdir():
        if file.is_dir():
            folders_list.append(file)
            view_folder(file) 
        else:
            select_file(file)
    folders_list.sort(key=lambda Path: len(Path.parts), reverse = True)


# ========== synchronous ===============
def write_dict(path):  # save files_dict, known_suffix, unknown_suffix
    count = 0
    with open(path / "TS_FileList.txt", 'w') as f:
        for categ in files_dict.keys():
            if len(files_dict[categ]) > 0:
                f.write(f'>>> {categ}\n')
                for file in files_dict[categ]:
                    f.write(f'{count:7}: {file}\n')  
                    count += 1
    print(f"write {count} files")

    with open(path / "TS_SuffixKnown.txt", 'w') as f:
        for suf in known_suffix:
            f.write(f'{suf}\n')

    with open(path / "TS_SuffixUnknown.txt", 'w') as f:
        for suf in unknown_suffix:
            f.write(f'{suf}\n')
    
    count = 0
    with open(path / "TS_FoldersList.txt", 'w') as f:
        for fold in folders_list:
            f.write(f'{count:5}: {len(fold.parts):2}  {fold}\n')
            count += 1
    print(f"write {count} folders")

# ============= threads ==================
def write_filelist_th(path):  # save files_dict
    count = 0
    with open(path / "TS_FileList.txt", 'w') as f:
        for categ in files_dict.keys():
            if len(files_dict[categ]) > 0:
                f.write(f'>>> {categ}\n')
                for file in files_dict[categ]:
                    f.write(f'{count:7}: {file}\n')  
                    count += 1
    print(f"write {count} files")
    # logging.debug('write_filelist_th: done')

def write_sufkn_th(path):   # save known_suffix
    with open(path / "TS_SuffixKnown.txt", 'w') as f:
        for suf in known_suffix:
            f.write(f'{suf}\n')
    # logging.debug('write_sufkn_th: done')       

def write_sufun_th(path):   # save unknown_suffix
    with open(path / "TS_SuffixUnknown.txt", 'w') as f:
        for suf in unknown_suffix:
            f.write(f'{suf}\n')
    # logging.debug('write_sufun_th: done')
    
def write_foldlist_th(path):  # save folders_list  
    count = 0
    with open(path / "TS_FoldersList.txt", 'w') as f:
        for fold in folders_list:
            f.write(f'{count:5}: {len(fold.parts):2}  {fold}\n')
            count += 1
    print(f"write {count} folders")
    # logging.debug('write_folflist_th: done')



def main_synchro():
    workpath = pathlib.Path(r"e:/PROG/PYTHON/")
    view_folder(workpath)
    write_dict(workpath)

    
def main_thread():
    workpath = pathlib.Path(r"e:/PROG/PYTHON/")

    t1 = Thread(target = view_folder, args=(workpath,))
    t1.start()
    t1.join()

    t2 = Thread(target = write_filelist_th, args=(workpath,))
    t2.start()
    t2.join()

    t3 = Thread(target = write_foldlist_th, args=(workpath,))
    t3.start()
    t3.join()
    
    t4 = Thread(target = write_sufun_th, args=(workpath,))
    t4.start()
    t4.join()
    
    t5 = Thread(target = write_sufkn_th, args=(workpath,))
    t5.start()
    t5.join()

   

if __name__ == "__main__":

    # logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    print(f"\n>> synchronous start")
    start = time.time()
    main_synchro()
    end = time.time()
    print(f">> General time main: {end - start}") 

    files_dict = {'images': [], 'video': [], 'documents': [], 'audio': [], 'archives': [], 'unknown': []}
    known_suffix = set()
    unknown_suffix = set()
    folders_list = []

    print(f"\n>> threads start")
    start = time.time()
    main_thread()
    end = time.time()
    print(f">> General time main_th: {end - start}\n") 



