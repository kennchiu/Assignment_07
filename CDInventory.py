#------------------------------------------#
# Title: CDInventory.py
# Desc: Working binary data and error/exception handling.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# KChiu, 2022-Mar-06, Updated codes to complete the Magic CD Inventory Program
# KChiu, 2022-Mar-13, Updated program to save output and read input as binary data and to add error handling functions.
#------------------------------------------#

# -- DATA -- #
import pickle # import modoule needed to pickling/unpickling
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    """Processing user input to add or delete CDs"""
    @staticmethod
    def add_cd(cd_id, cd_title, cd_artist):         
        """Function to add a new cd to lstTbl table if user chooses to

        Append the CD ID, Title and Artist Name of the new CD to the lstTbl table
        in a dictionary list format.

        Args:
            cd_id (integer): ID number of the new CD
            cd_title (string): Title of the new CD
            cd_artist (string): Arist name of the new CD            

        Returns:
            None.
        """
        # Add item to the lstTbl table
        dicRow = {'ID': intID, 'CD Title': cd_title, 'Artist': cd_artist}
        lstTbl.append(dicRow)
        
    @staticmethod
    def delete_cd(cd_id):         
        """Function to delete an existing cd if user chooses to

        Deleted the user chosen CD from the lstTbl table.
        An error is rasied to the user if the CD ID doesn't exist

        Args:
            cd_id (integer): ID number of the existing CD to be deleted

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == cd_id:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!\n')        

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage binary data ingestion from file to a list of dictionaries

        Reads the data in binary format from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the binary data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file        
        # read in CD inventory data in binary format with pickle module
        try:
            with open(file_name, 'rb') as objFile:
                dill_pickle = pickle.load(objFile)
                for row in dill_pickle:
                    dicRow = {'ID': int(row['ID']), 'CD Title': row['CD Title'], 'Artist': row['Artist']}
                    table.append(dicRow)
        except FileNotFoundError as e:# added error handling if CDInventory file doesn't exist.
            print('\nFileNotFoundError: ' + file_name +' File does not exist!')
            print(e, '\n')
    @staticmethod
    def write_file(file_name, table):
        """Function to sync the data in memory to file by saving current table in binary format
        
        Writes the data in the lstTbl in memory to the CDInventory.txt file in binary format.
        
        Args:
            file_name (string): name of file used to write/save the data to
            table (multiple lists): 2D data structure (values of multiple lists of dicts) 
                                    that holds the current data during runtime

        Returns:
            None.
        
        """
        # save data in binary format with pickle module
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)

# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] Load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to file\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
            if choice not in ['l', 'a', 'i', 'd', 's', 'x']:
                print('Please enter a valid option!')
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist        
        while True:
            #Convert ID to integer format since default user input is in string format
            strID = input('Enter ID: ').strip()
            try:
                intID = int(strID)
                break
            except ValueError as e: # added error handling if user provides a value that can't be converted to an integer
                print('ValueError: This is not an integer!')
                print(e, '\n')                
                continue
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? \n').strip()
        DataProcessor.add_cd(strID, strTitle, strArtist)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get User input for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:# continues to ask until an integer is provided.
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError as e:# added error handling if user provides a value that can't be converted to an integer
                print('\nValueError: This is not a valid CD ID! Please enter an integer.')
                print(e, '\n')                
                continue# start loop back and ask for an ID number.
        DataProcessor.delete_cd(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')