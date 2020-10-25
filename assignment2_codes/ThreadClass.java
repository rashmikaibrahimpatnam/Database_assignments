package assignment2_codes;

import java.sql.Connection;

public class ThreadClass implements Runnable{

	private Operations ops;
	private Connection connect;
	private String city;
	
	public ThreadClass(Operations ops, Connection connect, String city) {
		this.ops = ops;
		this.connect = connect;
		this.city = city;
	}
	
	@Override
	public void run() {
		ops.perform_trans(connect,city);			
	}

}
