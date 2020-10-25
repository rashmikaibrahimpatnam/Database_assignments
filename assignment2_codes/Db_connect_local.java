package assignment2_codes;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Db_connect_local {
	private String dburl = "jdbc:mysql://localhost:3306/olist_local";
	private String user = "root";
	private String password = "Sai@9697";
	Connection connect;
	
	public Connection connect_local() {
		try{
            try {
				Class.forName("com.mysql.cj.jdbc.Driver");
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
			}
            connect = DriverManager.getConnection(dburl,user,password);
            System.out.println("connected to the local database");   
            return connect;
            
        }
        catch(SQLException e){
        	e.printStackTrace();
        }
		return connect;
	}
	
	public void disconnect_local(Connection cnt) {
		try {
			cnt.close();
			System.out.println("disconnected from the local database");
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
