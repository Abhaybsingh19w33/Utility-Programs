package emailScriptPackage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
//import org.openqa.selenium.WebDriverManager;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
public class EmailClass {
    public static void main(String[] args) {
  
//        // Step 2- Execute Selenium test on port 9222
//
//        // set the driver path- You can also use WebDriverManager for drivers
//        System.setProperty("webdriver.chrome.driver","F:\\chromedriver_win32\\chromedriver.exe");
//
//        // Create object of ChromeOptions Class
//        ChromeOptions opt=new ChromeOptions();
//
//        // pass the debuggerAddress and pass the port along with host. Since I am running test on local so using localhost
//        opt.setExperimentalOption("debuggerAddress","127.0.0.1:9222");
//
//        // pass ChromeOptions object to ChromeDriver constructor
//        WebDriver driver=new ChromeDriver(opt);
//
//        // now you can use now existing Browser
//        driver.get("http://facebook.com");
//        
        
        ChromeOptions options = new ChromeOptions(); 
        options.setExperimentalOption("debuggerAddress", "127.0.0.1:9222");
//        options.addArguments("--remote-allow-origins=*");
        options.addArguments("--remote-allow-origins=*","ignore-certificate-errors");
//        WebDriverManager.chromedriver().setup();
        WebDriver driver = new ChromeDriver(options); 
        driver.get("https://abodeqa.com/contact-us/");
        //name field on contact us page of abodeqa 
        driver.findElement(By.id("g1280-name")).sendKeys("abodeqa"); 
        //Email id field 
        driver.findElement(By.id("g1280-email")).sendKeys("abodeqa@gmail.com"); 
        //website 
        driver.findElement(By.id("g1280-website")).sendKeys("https://abodeqa.com"); 
        //comment. 
        driver.findElement(By.id("contact-form-comment-g1280-comment")).sendKeys("This is one sample comment.");
    }
}


