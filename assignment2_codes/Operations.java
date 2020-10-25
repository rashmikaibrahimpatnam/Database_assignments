package assignment2_codes;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class Operations{
	
	
	public void perform_trans(Connection conn, String city) {
		
		//read data
		String read_data = "select * from customers where customer_zip_code_prefix = 01151";
		//update data
		String update_data = "update geolocation set geolocation_city = ? where geolocation_zip_code_prefix = 01151";
		
		
		
		try {
			PreparedStatement read = conn.prepareStatement(read_data);
			PreparedStatement update = conn.prepareStatement(update_data);
			conn.setAutoCommit(false);
			ResultSet res = read.executeQuery();
			if(res!= null) {
				update.setString(1, city);
				int up = update.executeUpdate();
				if(up == 1) {
					System.out.println("city updated to "+city);
				}
			}
			
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
	}
	
	
	public void distributed_trans(Connection locconnect, Connection rmtconnect, String state, String title,String city,String seller_id ) {
		//update data 1
		String update_state = "update geolocation set geolocation_state = ? where geolocation_city = 'T1 City'";
		//update data 2
		String update_review_title = "update reviews set review_comment_title = ? where review_comment_message = 'Excelente produto.'";		
		
		//insert seller data
		String insert_seller = "insert into sellers values (?, 69900,'rio branco','AC')" ;
		
		//update seller data
		String update_seller ="update sellers set seller_city = ? where seller_zip_code_prefix = 69900";
				
		//delete seller data
		String select_seller = "select * from sellers where seller_id = '4be2e7f96b4fd749d52dff41f80e39dd' for update";
		
		try {
			//local updations
			PreparedStatement up_st = locconnect.prepareStatement(update_state);
			PreparedStatement up_rv = locconnect.prepareStatement(update_review_title);
			up_st.setString(1, state);
			int check = up_st.executeUpdate();
			if(check == 1) {
				System.out.println("Updated state in local database to "+state);
			}
			up_rv.setString(1, title);
			int flg = up_rv.executeUpdate();
			if(flg == 1) {
				System.out.println("review title updated in local database to "+title);
			}
			
			//remote operations
			PreparedStatement ins = rmtconnect.prepareStatement(insert_seller);
			PreparedStatement upd = rmtconnect.prepareStatement(update_seller);
			PreparedStatement sec = rmtconnect.prepareStatement(select_seller);
			ins.setString(1, seller_id);
			boolean val = ins.execute();
			if(val) {
				System.out.println("new seller data is inserted into sellers table ");
			}
			upd.setString(1, city);
			int up = upd.executeUpdate();
			if(up == 1) {
				System.out.println("updated seller_city in sellers table to "+city);
			}
			ResultSet res = sec.executeQuery();
			while(res.next()) {
				System.out.println(res.getString("seller_id"));
				System.out.println(res.getInt("seller_zip_code_prefix"));
				System.out.println(res.getString("seller_city"));
				System.out.println(res.getString("seller_state"));
			}
			
			
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	

}
