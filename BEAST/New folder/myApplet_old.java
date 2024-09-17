import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class myApplet extends java.applet.Applet {
    public void init() {
        try {
            // URL to send the POST request to
            URL url = new URL("http://127.0.0.3:5000/aaaaaaaaaaa");

            // Open a connection to the URL
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            // Set the request method to POST
            connection.setRequestMethod("POST");

            // Enable input and output streams
            connection.setDoOutput(true);

            connection.setRequestProperty("Content-Type", "text/plain");
            connection.setFixedLengthStreamingMode(16);
            connection.connect();

            // Data to send in the POST request body
            String urlParameters = "0123456789abcdef";

            // Send the POST request
            OutputStream os = connection.getOutputStream();
            connection.connect();
            Thread.sleep(5000);
            os.write(urlParameters.getBytes());
            os.flush();
            os.close();

            // Get the response from the server
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuffer content = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
            in.close();
            
            // Handle the response (e.g., print it or process it as needed)
            System.out.println(content.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
