class Names():
    
    class Select():
        
        definition = "select_smth"
        varSelectTable = "select_source"
        varWhereExpr = "where_expr"  
              
        class ColumnsLevel():
            levelName = "column_name"
            varTableName = "table_name"
            varColumnName = "column_name"            
        
    class Create():       
        
        definition = "create_table"        
        flagTemp = "temp"
        flagIfNotExists = "if_not_exists"
        varDatabaseName = "database_name"
        varTableName = "table_name"
        
        class ColumnsLevel():
            levelName = "column_def"
            varColumnName = "column_name"
            varColumnType = "type_name"
            varColumnSize = "type_size"
            varColumnDefaultValue = "default_value"
            varColumnDefaultExpr = "default_expr"
            varColumnCheckExpr = "check_expr"
            flagAutoinc = "autoincrement"
            flagPrimary = "primary_key"
            flagNotNull = "not_null"
            flagUnique = "unique"
        
    class Insert():
        
        definition = "insert_smth"      
        flagRollback = "rollback"
        flagAbort = "abort"
        flagReplace = "replace"
        flagFail = "fail"
        flagIgnore = "ignore"   
        varDatabaseName = "database_name"
        varTableName = "table_name"        
        varInsertFromSelectExpr = "selection"
        
        class ColumnsLevel():
            levelName = "column_name"
            varTableName = "table_name"
            varColumnName = "column_name"
        
        class ValuesLevel():
            levelName = "insert_values"
            varValue = "value"
            
    class Delete():
        
        definition = "delete_smth"
        varDatabaseName = "database_name"
        varTableName = "table_name"
        varWhereExpr = "where_expr"
        
    class Update():
        
        definition = "update_smth"
        
        flagRollback = "rollback"
        flagAbort = "abort"
        flagReplace = "replace"
        flagFail = "fail"
        flagIgnore = "ignore" 
        
        varTableName = "table_name"
        varWhereExpr = "where_expr"
        
        class ColumnsLevel():
            levelName = "update_set"
            varColumnName = "column_name"
            varColumnUpdateExpr = "column_update_expr"
            
    class Expression():
        
        definition = "expression"
        
        class UnaryOperator():
            varUnaryOperator = "unary_operator"
            varUnaryExpression = "unary_expression"
            
        class BinaryOperator():
            varBinaryLeft = "binary_left"
            varBinaryRight = "binary_right"
            varBinaryOperator = "binary_operator"
            
        class Like():
            varLikeLeft = "like_left"
            varLikeRight = "like_right"
            flagReverse = "not"
            flagLike = "like"
            flagMatch = "match"
            
        class Null():
            varNullValue = "null_check_val"
            flagIsNull = "isnull"
            flagNotNull = "notnull"
        
        class Is():
            varIsLeft = "is_left"
            varIsRight = "is_right"
            flagReverse = "not"
            
        class Between():
            varBetweenValue = "between_val"
            varBetweenLeft = "between_left"
            varBetweenRight = "between_right"
            varBetweenReversed = "not"

class Definitions():
               
    column_def = "{column_name} >>type_name >>column_constraint"
    type_name = "{type_name} ?[({type_size})]"
    table_name = "?[{database_name}.]{table_name}"
    insert_values = "{value}"
    column_name = "?[{table_name}.]{column_name}"
                   
    create_table = """    
    CREATE {temp:TEMPORARY} TABLE {if_not_exists:IF NOT EXISTS}
    >>table_name
    ( #>>column_def @,# )
    """
    
    column_constraint = """
    {primary_key: PRIMARY KEY}
    {autoincrement: AUTOINCREMENT}
    {not_null: NOT NULL}
    {unique: UNIQUE}
    ?[CHECK ({check_expr})]
    ?[DEFAULT [{default_value}|{default_expr}]]
    """   

    insert_smth = """
    INSERT >>error
    INTO >>table_name ?[(#>>column_name @,#)] [ VALUES ( #>>insert_values @,# ) | {selection} ]
    """
    
    error = """
       {rollback: OR ROLLBACK}
       {abort: OR ABORT}
       {replace: OR REPLACE}
       {fail: OR FAIL}
       {ignore : OR IGNORE}
    """

    select_smth = """
    >>select_core ?[ORDER BY >>ordering_term] ?[LIMIT {limit} ?[OFFSET {offset}]]
    """   
     
    ordering_term = "{ignore_this_now}"
        
    select_core = """
    SELECT [#>>column_name @,# | * ]
    FROM {select_source}
    ?[WHERE {where_expr}]
    """
    
    delete_smth = "DELETE FROM >>table_name ?[WHERE {where_expr}]"

    update_smth = """
    UPDATE >>error >>table_name
    SET #>>update_set @,#
    ?[WHERE {where_expr}]
    """
    
    update_set = "{column_name} = {column_update_expr}"
    
    expression = """[ 
    {value} | 
    {unary_operator} {unary_expression} |
    {binary_left} {binary_operator} {binary_right} |
    {function_name} ( ?[#>>function_arg @,#] ) |
    {like_left} {not:NOT} {like:LIKE}{match:MATCH} {like_right} |
    {null_check_val} {isnull: ISNULL} {notnull:NOT NULL} |
    {is_left} IS {not:NOT} {is_right} |
    {between_val} {not:NOT} BETWEEN {between_left} AND {between_right} ]
    """
    
    function_arg = "{ignore_this_now}"
    
