import os, psutil, time

def ret_disks():
    result = []
    for dev in psutil.disk_io_counters(perdisk=True):
        result.append("/dev/" + dev)
    return result


# Used patented techology Govnocode(R) Lite Edition


def read_disk(disk):
    block_size = 16 * 1024 # one sector in ATA is 512 bytes, but it be too slow
    mst_skip, print_threshold = 1, 0
    
    
    with open(disk, 'rb') as disk: #skull method, todo use mmap.mmap(infile, 0, access=mmap.ACCESS_READ) or native read from ata
        while True:
            if sum(disk.read(block_size)) != 0:
                print("[*] Here is some data on {} ({})".format(hex(disk.tell()), str(round(disk.tell()/1024/1024/1024, 2)) + "gb"))
                mst_skip = 1
            else:
                if mst_skip < 64: mst_skip += 0.001

            if print_threshold > 0x2f: print("> {}mb, skipstep: {}x".format(round(disk.tell()/1024/1024, 2), round(mst_skip, 2)), end='\r', flush=1); print_threshold = 0
            
            disk.seek(block_size * int(mst_skip), os.SEEK_CUR); print_threshold += 1
        
def main():
    if os.geteuid() != 0: print("Run as sudo."); return
    
    disks = ret_disks()
    print("\n".join(f"{a+1}. {b}" for a, b in enumerate(disks)))
    
    read_disk(disks[int(input("\nSelect disk: "))-1])
    
if __name__ == "__main__":
    main()
