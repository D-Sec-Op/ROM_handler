import os
import shutil
import zipfile
import py7zr
from scp import SCPClient
import paramiko

new_zips = (r"C:\Users\USERNAME\Desktop\ROM_zips\fresh")                # These must be bottom level directories
unzipped = (r"C:\Users\USERNAME\Desktop\ROM_zips\loaded")               # If they contain sub-directories
unsorted_roms = (r"C:\Users\USERNAME\Desktop\ROM_zips\ROMS\unsorted")   # os.walk will cause errors as written
sorting_path = (r"C:\Users\USERNAME\Desktop\ROM_zips\ROMS")
usb_storage = (r"D:\retropie\roms")


def unzipper():
    print("Unzipping ROM files in", new_zips)
    for root, dirs, files in os.walk(new_zips):
        for file in files:
            if file.endswith(r".zip"):
                print("Unzipping", str(file))
                with zipfile.ZipFile(new_zips+"\\"+file) as zipObj:
                    zipObj.extractall(unsorted_roms)
                shutil.move(new_zips+"\\"+file, unzipped)
            if file.endswith(r".7z"):
                shutil.move(root + '\\' + file, unsorted_roms)
    print("All files unzipped, zipped folders moved to", unzipped)
    choice = input("Would you like to perform another task?(y/n)")
    if choice.lower() == 'y':
        selector()
    else:
        print("Exiting program...")

def sort_roms_local():
    print("Sorting ROM files in", unsorted_roms)
    for root, dirs, files in os.walk(unsorted_roms):
        for file in files:
            if file.endswith(".md"):
                shutil.move(root + '\\' + file, sorting_path + r'\md\\' + file)
            elif file.endswith(".n64"):
                shutil.move(root + '\\' + file, sorting_path + r'\N64\\' + file)
            elif file.endswith(".nes"):
                shutil.move(root + '\\' + file, sorting_path + r'\NES\\' + file)
            elif file.endswith(".sfc"):
                shutil.move(root + '\\' + file, sorting_path + r'\SNES\\' + file)
            elif file.endswith(".gba"):
                shutil.move(root + '\\' + file, sorting_path + r'\gba\\' + file)
            elif file.endswith(".gb"):
                shutil.move(root + '\\' + file, sorting_path + r'\gb\\' + file)
            elif file.endswith(r".7z"):
                shutil.move(root + '\\' + file, sorting_path + r'\psx\\' + file)
    print("All ROM files sorted locally.")
    choice = input("Would you like to perform another task?(y/n)")
    if choice.lower() == 'y':
        selector()
    else:
        print("Exiting program...")

def copy_to_drive():
    if os.path.isdir(usb_storage):
        print("Copying ROMs to external storage at:", usb_storage)
        for root, dirs, files in os.walk(unsorted_roms):
            for file in files:
                if file.endswith(".md"):
                    print("Copying", file, "to external storage")
                    shutil.copy2(root + '\\' + file, usb_storage + r'\megadrive\\' + file)
                elif file.endswith(".n64"):
                    print("Copying", file, "to external storage")
                    shutil.copy2(root + '\\' + file, usb_storage + r'\n64\\' + file)
                elif file.endswith(".nes"):
                    print("Copying", file, "to external storage")
                    shutil.copy2(root + '\\' + file, usb_storage + r'\nes\\' + file)
                elif file.endswith(".sfc"):
                    print("Copying", file, "to external storage")
                    shutil.copy2(root + '\\' + file, usb_storage + r'\snes\\' + file)
                elif file.endswith(".gba"):
                    print("Copying", file, "to external storage")
                    shutil.copy2(root + '\\' + file, usb_storage + r'\gba\\' + file)
                elif file.endswith(".gb"):
                    print("Copying", file, "to external storage")
                    shutil.copy2(root + '\\' + file, usb_storage + r'\gb\\' + file)
                elif file.endswith(r".7z"):
                    with py7zr.SevenZipFile(root + '\\' + file, 'r') as zipfile:
                        zipfile.extractall(path= usb_storage + r'\psx\\' + file)
        print("All files copied to external storage.")
        choice = input("Would you like to perform another task?(y/n)")
        if choice.lower() == 'y':
            selector()
        else:
            print("Exiting program...")
    else:
        print("Error locating drive, exiting program to protect data...")

def scp_to_pie():
    choice = input("Please ensure retropie is powered on and connected to the network(y to continue, q to return to menu)")
    if choice == 'y':
        password = input("Enter RetroPie password:")
        pie_path = r'/home/RetroPie/roms/megadrive'

        def createSSHClient(server, port, user, password):
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, port, user, password)
            return client

        ssh = createSSHClient('retropie', 22, 'pi', password)
        scp = SCPClient(ssh.get_transport())

        print("Copying ROMs by SCP to RetroPie")
        for root, dirs, files in os.walk(unsorted_roms):
            for file in files:
                if file.endswith(".md"):
                    print("Copying", file, "to Pi")
                    scp.put()
                    # shutil.copy2(root + '\\' + file, usb_storage + r'\megadrive\\' + file)


    elif choice == 'q':
        selector()
    else:
        print("Invalid selection, try again")
        scp_to_pie()

def selector():
    choice = int(input(
        "Would you like to:\n\tUnzip newly downloaded ROMs?[1]\n\tCopy new ROMs to D:?[2]\n\tSort ROMS locally by console?[3]\n\tQuit[0]"))

    if choice == 1:
        unzipper()
    elif choice == 2:
        copy_to_drive()
    elif choice == 3:
        sort_roms_local()
    elif choice == 0:
        print("Exiting program...")
    else:
        print("Invalid selection, try again")
        selector()

def main():
    selector()



if __name__ == "__main__":
    main()

