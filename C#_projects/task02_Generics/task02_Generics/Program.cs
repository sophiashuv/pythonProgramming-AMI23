using System;
using System.Reflection;

namespace task02_Generics
{
    class MainClass
    {
        private static void read_txt_file<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            Console.WriteLine("Enter file_name: ");
            var file = Validation.ValidateFile(Console.ReadLine());
            if (file.EndsWith(".txt")) l.ReadTxtFile(file);
            else l.ReadJsonFile(file);
        }
        
        private static void sort_elements<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            Console.WriteLine("Enter field for which you want to sort: \n" +
                              "POSSIBLE: Title, Image_url, Price, Created_at, " +
                              "Updated_at, Description, Id:\n");
            l.Sort(Console.ReadLine());
        }
        
        private static void search_elements<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            Console.WriteLine("Enter parameter which elements you want to find: \n");
            var res = new LstCollection<T>(l.Search(Console.ReadLine()));
            Console.WriteLine(res);
        }
        
        private static void add_elements<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            var p = new T();
            p.Input();
            l.AddItem(p);
        }
        
        private static void del_element<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            Console.WriteLine("Enter id to delete: ");
            l.Delete(Console.ReadLine());
        }
        
        private static void edit_element<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            Console.Write("Enter id to edit: ");
            var id = Console.ReadLine();
            Console.Write("Enter atter to edit: ");
            var atter = Console.ReadLine();
            Console.Write("Enter value to change: ");
            var value = Console.ReadLine();
            l.Edit(id, atter, value);
        }
        
        private static void write_file<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            Console.WriteLine("Enter file_name: ");
            var file = Validation.ValidateFile(Console.ReadLine());
            if (file.EndsWith(".txt")) l.WriteTxtFile(file);
            else l.WriteJsonFile(file);
        }
        
        private static void add_txt_file<T>(LstCollection<T> l) where T: BaseClass, new()
        {
            Console.WriteLine("Enter file_name: ");
            l.AddToTxtFile(Validation.ValidateFile(Console.ReadLine()));
        }
        
        private static string get_help_message()
        {
            string helpMessage = new string('*', 51);
            helpMessage += "\n*  HELP:" + new string(' ', 42) + "*\n*  Possible commands:" + new string(' ', 29) +
                            "*\n*  1 - to read from file;" + new string(' ', 25) +
                            "*\n*  2 - to sort elements; " + new string(' ', 25) +
                            "*\n*  3 - to to search element.  " + new string(' ', 20) +
                            "*\n*  4 - to to add element to collection. " + new string(' ', 10) +
                            "*\n*  5 - to del element from collection.  " + new string(' ', 10) +
                            "*\n*  6 - to edit element from collection.  " + new string(' ', 9) +
                            "*\n*  7 - to write collection elements to file.      " +
                            "*\n*  8 - to add  collection elements to txt file.   " +
                            "*\n*  9 - to print collection. " + new string(' ', 22) +
                            "*\n*  exit - to exit.  " + new string(' ', 30) + "*\n";
            helpMessage += new string('*', 51) + "\n";
            return helpMessage;
        }

        public static void Main(string[] args)
        {
            LstCollection<Product> l = new LstCollection<Product>();
            while (true) 
            {
                Console.WriteLine(get_help_message());
                string task = Console.ReadLine();
                switch (task)
                {
                    case "1":
                        Validation.ValidateInput(l, read_txt_file);
                        break;
                    case "2":
                        Validation.ValidateInput(l, sort_elements);
                        break;
                    case "3":
                        Validation.ValidateInput(l, search_elements);
                        break;
                    case "4":
                        Validation.ValidateInput(l, add_elements);
                        break;
                    case "5":
                        Validation.ValidateInput(l, del_element);
                        break;
                    case "6":
                        Validation.ValidateInput(l, edit_element);
                        break;
                    case "7":
                        Validation.ValidateInput(l, write_file);
                        break;
                    case "8":
                        Validation.ValidateInput(l, add_txt_file);
                        break;
                    case "9":
                        Console.WriteLine(l);
                        break;
                    case "exit":
                        Console.WriteLine("GOODBYE!");
                        return;
                    default:
                        Console.WriteLine("WRONG INPUT!");
                        continue;
            }
                Console.WriteLine();
            } 
        }
    }
}