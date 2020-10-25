package assignment2_codes;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.Scanner;

public class MainClass {

	public static void sequence() {
		String t1_city = "T1 City";
		String t2_city = "T2 City";

		//for transaction 1
		Db_connect_local dcl1 = new Db_connect_local();
		Connection conn = dcl1.connect_local();

		//for transaction 2
		Db_connect_local dcl2 = new Db_connect_local();
		Connection conn2 = dcl2.connect_local();

		Operations ops = new Operations();

		Runnable rb = new ThreadClass(ops,conn,t1_city);
		Runnable rb2 = new ThreadClass(ops,conn2,t2_city);

		Thread t1 = new Thread(rb);
		Thread t2 = new Thread(rb2);

		t1.start();
		t2.start();

		try {
			try {
				t2.join();
				conn2.commit();		
				t1.join();
				conn.commit();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			try {
				if(conn != null || conn2 != null) {
					conn.rollback();
					conn2.rollback();
				}
			} catch (SQLException e1) {
				e1.printStackTrace();
			}
		}
		finally {

			dcl1.disconnect_local(conn);
			dcl2.disconnect_local(conn2);
		}


	}

	public static void distributed() throws SQLException {


		//for transaction 1
		Db_connect_local loc = new Db_connect_local();
		Connection conn_loc = loc.connect_local();
		Db_connect_remote rmt = new Db_connect_remote();
		Connection conn_rmt = rmt.connect_remote();
		conn_loc.setAutoCommit(false);
		conn_rmt.setAutoCommit(false);
		String state1 = "TC";
		String title1 = "Excelente";
		String city1 = "halifax";
		String sellerid1 = "4be2e7f96b4fd749d52dff41f80e39dd";


		//for transaction 2
		Db_connect_local loc2 = new Db_connect_local();
		Connection conn_loc2 = loc2.connect_local();
		Db_connect_remote rmt2 = new Db_connect_remote();
		Connection conn_rmt2 = rmt2.connect_remote();
		conn_loc2.setAutoCommit(false);
		conn_rmt2.setAutoCommit(false);
		String state2 = "T1";
		String title2 = "Excelente produto.";
		String city2 = "kitchener";
		String sellerid2 = "newid";

		Operations oper = new Operations();
		Runnable rn = new DistributedClass(oper, conn_loc, conn_rmt,state1,title1,city1,sellerid1);
		Runnable rn2 = new DistributedClass(oper, conn_loc2, conn_rmt2,state2,title2,city2,sellerid2);

		Thread t1 = new Thread(rn);
		Thread t2 = new Thread(rn2);

		t1.start();
		t2.start();		
		try {
			try {
				t2.join();
				conn_loc2.commit();
				conn_rmt2.commit();
				t1.join();
				conn_loc.commit();
				conn_rmt.commit();				
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			if(conn_loc != null || conn_rmt != null || conn_loc2 != null || conn_rmt2 != null) {
				try {
					conn_loc.rollback();
					conn_rmt.rollback();
					conn_loc2.rollback();
					conn_rmt2.rollback();
				} catch (SQLException e1) {
					e1.printStackTrace();
				}

			}

		}
		finally {
			loc.disconnect_local(conn_loc);
			loc2.disconnect_local(conn_loc2);
			rmt.disconnect_remote(conn_rmt);
			rmt2.disconnect_remote(conn_rmt2);
		}





	}
	public static void main(String args[]){
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter sequence or distributed: ");
		String choice = sc.nextLine();
		if (choice != null) {
			switch(choice.toLowerCase()) {
			case "sequence":
				sequence();
				break;
			case "distributed":
				try {
					distributed();
				} catch (SQLException e) {
					e.printStackTrace();
				}
				break;
			default:
				System.out.println("please enter appropriate choice");				
			}
		}



	}
}
