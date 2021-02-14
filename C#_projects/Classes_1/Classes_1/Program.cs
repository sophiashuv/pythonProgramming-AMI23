using System;

namespace Classes_1
{
    class MainClass
    {
        private static void read_txt_file(LstCollection l)
        {
            Console.WriteLine("Enter file_name: ");
            var file = Validation.ValidateFile(Console.ReadLine());
            if (file.EndsWith(".txt")) l.ReadTxtFile(file);
            else l.ReadJsonFile(file);
        }
        
        private static void sort_elements(LstCollection l)
        {
            Console.WriteLine("Enter field for which you want to sort: \n" +
                              "POSSIBLE: Title, Image_url, Price, Created_at, " +
                              "Updated_at, Description, Id:\n");
            l.Sort(Console.ReadLine());
        }
        
        private static void search_elements(LstCollection l)
        {
            Console.WriteLine("Enter parameter which elements you want to find: \n");
            var res = new LstCollection(l.Search(Console.ReadLine()));
            Console.WriteLine(res);
        }
        
        private static void add_elements(LstCollection l)
        {
            var p = new Product();
            p.InputProduct();
            l.AddItem(p);
        }
        
        private static void del_product(LstCollection l)
        {
            Console.WriteLine("Enter id to delete: ");
            l.Delete(Console.ReadLine());
        }
        
        private static void edit_product(LstCollection l)
        {
            Console.Write("Enter id to edit: ");
            var id = Console.ReadLine();
            Console.Write("Enter atter to edit: ");
            var atter = Console.ReadLine();
            Console.Write("Enter value to change: ");
            var value = Console.ReadLine();
            l.Edit(id, atter, value);
        }
        
        private static void write_file(LstCollection l)
        {
            Console.WriteLine("Enter file_name: ");
            var file = Validation.ValidateFile(Console.ReadLine());
            if (file.EndsWith(".txt")) l.WriteTxtFile(file);
            else l.WriteJsonFile(file);
        }
        
        private static void add_txt_file(LstCollection l)
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
                            "*\n*  4 - to to add Product to collection. " + new string(' ', 10) +
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
            LstCollection l = new LstCollection();
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
                        Validation.ValidateInput(l, del_product);
                        break;
                    case "6":
                        Validation.ValidateInput(l, edit_product);
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