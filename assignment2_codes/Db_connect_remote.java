package assignment2_codes;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Db_connect_remote {
	private String dburl = "jdbc:mysql://35.221.10.205:3306/olist_remote";
	private String user = "root";
	private String password = "Sai@9697";
	Connection connect;
	
	public Connection connect_remote() {
		try{
            try {
				Class.forName("com.mysql.cj.jdbc.Driver");
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
			}
            connect = DriverManager.getConnection(dburl,user,password);
            System.out.println("connected to the remote database");   
            return connect;
            
        }
        catch(SQLException e){
        	e.printStackTrace();
        }
		return connect;
	}
	
	public void disconnect_remote(Connection cnt) {
		try {
			cnt.close();
			System.out.println("disconnected from the remote database");
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
