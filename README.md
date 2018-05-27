# contacts-basic
A url map for the above app

Map([

<Rule '/contacts/delete' (OPTIONS, DELETE) -> contactBook.delete_contact>,

<Rule '/contacts/search' (POST, OPTIONS) -> contactBook.search>,

<Rule '/contacts/edit' (POST, OPTIONS) -> contactBook.edit_contact>,

<Rule '/contacts/add' (POST, OPTIONS) -> contactBook.add_contact>,

<Rule '/user/addUser' (POST, OPTIONS) -> auth.new_user>,

<Rule '/user/token' (POST, OPTIONS) -> auth.get_auth_token>,

<Rule '/contacts/' (HEAD, POST, OPTIONS, GET) -> contactBook.test>,

<Rule '/static/' (HEAD, OPTIONS, GET) -> static>])