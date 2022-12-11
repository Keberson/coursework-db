UPDATE internal_user
SET user_group = '$input_group', login = '$input_login', password = '$input_password'
    where user_id = '$user_id'