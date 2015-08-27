import java.io.*;
import java.util.*;

public class OrganizeItems {
    public static void main(String[] args) throws IOException{
        BufferedReader reader = new BufferedReader(new FileReader("listofitems.txt"));
        String current = "";
        String totalName = "";
        String totalVal = "";
        String[] names = new String[289];
        int[] values = new int[289];
        int count = 0;
        while ((current = reader.readLine()) != null) {
            totalVal += current.substring(current.length() - 4, current.length()) + ",";
            current = current.substring(0, current.length() - 4);
            int max = 0;
            for(int i = current.length() - 1; i >= 0; i--)
                if(current.charAt(i) == ' ')
                    max = i;
                else
                    break;
            current = current.substring(0, max);
            for(int i = 0; i < current.length(); i++)
                if(current.charAt(i) == '\'') {
                    current = current.substring(0, i) + "\\" + current.substring(i, current.length());
                    break;
                }
            totalName += "\'" + current + "\',";
            count++;
        }
        PrintWriter writer = new PrintWriter("listofitems.min", "UTF-8");
        writer.println(totalName);
        writer.println(totalVal);
        writer.close();
    }
}