from xtreme_library.excel_creator import create_excel

list_data = [
    {
        'name' : 'sam',
        'age' : 20,
        'status': 'PASS'
    },
{
        'name' : 'MAX',
        'age' : 23,
        'status': 'PASS'
    }
]
c = create_excel(list_data,'mack.xlsx',"sample")