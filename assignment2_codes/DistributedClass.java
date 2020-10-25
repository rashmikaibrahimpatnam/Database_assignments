package assignment2_codes;

import java.sql.Connection;

public class DistributedClass implements Runnable{

	private Operations oper;
	private Connection locconnect;
	private Connection rmtconnect;
	private String state;
	private String title;
	private String city;
	private String seller_id;
	
	public DistributedClass(Operations oper, Connection locconnect, Connection rmtconnect, String state, String title, String city, String seller_id) {
		this.oper = oper;
		this.locconnect = locconnect;
		this.rmtconnect = rmtconnect;
		this.state = state;
		this.title = title;
		this.city = city;	
		this.seller_id = seller_id;
	}
	
	@Override
	public void run() {
		oper.distributed_trans(locconnect,rmtconnect,state,title,city,seller_id);
	}
	

}
