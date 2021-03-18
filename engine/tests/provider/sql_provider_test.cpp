#include "tests/utilities/BlazingUnitTest.h"
#include "io/data_provider/sql/MySQLDataProvider.h"
#include "io/data_parser/sql/MySQLParser.h"

struct MySQLProviderTest : public BlazingUnitTest {};

TEST_F(MySQLProviderTest, select_all) {
  std::cout << "TEST\n";

	ral::io::sql_connection sql_conn = {
		.host = "localhost",
		.port = 33060,
		.user = "lucho",
		.password = "admin",
		.schema = "employees"};

  auto mysql_provider = std::make_shared<ral::io::mysql_data_provider>(sql_conn, "departments", 2);

  int rows = mysql_provider->get_num_handles();

  std::cout << "\trows: " << rows << "\n";
  auto handle = mysql_provider->get_next();
  auto res = handle.sql_handle.mysql_resultset;
  
  bool has_next = mysql_provider->has_next();
  std::cout << "\tNEXT?: " << (has_next?"TRUE":"FALSE") << "\n";
  
  std::cout << "\tTABLE\n";
  while (res->next()) {
    std::cout << "\t\t" << res->getString("dept_no") << "\n";
  }

  std::cout << "PARSERRRRRRRRRRRRRRRRRRRRRRR\n";
  
  ral::io::mysql_parser parser;
  ral::io::Schema schema;
  parser.parse_schema(handle, schema);
  
  auto cols = schema.get_names();
  std::cout << "total cols: " << cols.size() << "\n";
  for (int i = 0; i < cols.size(); ++i) {
    std::cout << "\ncol: " << schema.get_name(i) << "\n";
    std::cout << "\ntyp: " << (int32_t)schema.get_dtype(i) << "\n";
  }


//  if(mysql_provider->has_next()){
//      ral::io::data_handle new_handle;
//      try{
//          std::cout << "mysql_provider->get_next" << "\n";
//          new_handle = mysql_provider->get_next();
//          std::cout << "mysql_provider->get_next (DONE)" << "\n";
//      }
//      catch(...){
//          std::cout << "mysql_provider->get_next (FAIL)" << "\n";
//          FAIL();
//      }
//      try{
//          bool is_valid = new_handle.is_valid();
//          std::cout << "ral::io::data_handle.valid (DONE) " << is_valid << "\n";
          
//          bool empty_uri = new_handle.uri.isEmpty();
//          std::cout << "ral::io::data_handle.uri.isEmpty (DONE) " << empty_uri << "\n";
          
//          bool valid_uri = new_handle.uri.isValid();
//          std::cout << "ral::io::data_handle.uri.isValid (DONE) " << valid_uri << "\n";

//          bool null_filehandle = (new_handle.file_handle == nullptr);
//          std::cout << "ral::io::data_handle.uri.file_handle is null (DONE) " << null_filehandle << "\n";
          
//          bool empty_column_values = new_handle.column_values.empty();
//          std::cout << "ral::io::data_handle.column_values.empty (DONE) " << empty_column_values << "\n";
//      }
//      catch(...){
//          std::cout << "ral::io::data_handle ops (FAIL)" << "\n";
//          FAIL();
//      }
//  }
}
