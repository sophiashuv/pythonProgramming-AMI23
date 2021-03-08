using System;
using System.Data;
using System.Threading.Tasks;
using MySqlConnector;

namespace API_03.Models
{
    public class ProductItem
    {

        private string title, created_at, updated_at, image_url, description;
        private double price;

        public long Id { get; set; }

        public string Description {
            get => description;
            set => description = value;
        }

        public string Title
        {
      
            get => title;
            set => title = Validation.ValidateTitle(value);
            
        }

        public string Image_url
        {
            get => image_url;
            set => image_url = Validation.ValidateImage_url(value);
        }

        public double Price
        {
            get => Math.Round(price, 2);
            set => price = Validation.ValidatePrice(value);
            //set => price = value;
        }

        public string Created_at
        {
            get => created_at;
            set => created_at = Validation.ValidateDate(value);
        }

        public string Updated_at
        {
            get => updated_at;
            set => updated_at = Validation.ValidateDate(created_at, value);
        }

        internal AppDb Db { get; set; }

        public ProductItem()
        {
        }

        internal ProductItem(AppDb db)
        {
            Db = db;
        }

        public async Task InsertAsync()
        {
            using var cmd = Db.Connection.CreateCommand();
            cmd.CommandText = @"INSERT INTO `product` (`_title`, `_price`, `_image_url`, `_created_at`, `_updated_at`, `description`) VALUES (@title, @price, @image_url, @created_at, @updated_at, @description);";
            BindParams(cmd);
            await cmd.ExecuteNonQueryAsync();
            Id = (int)cmd.LastInsertedId; 
        }

        public async Task UpdateAsync()
        {
            using var cmd = Db.Connection.CreateCommand();
            cmd.CommandText = @"UPDATE `product` SET `_title` = @title, `_price` = @price, `_image_url` = @image_url, `_created_at` = @created_at, `_updated_at` = @updated_at, `description` = @description WHERE `id` = @id;";
            BindParams(cmd);
            BindId(cmd);
            await cmd.ExecuteNonQueryAsync();
        }

        public async Task DeleteAsync()
        {
            using var cmd = Db.Connection.CreateCommand();
            cmd.CommandText = @"DELETE FROM `product` WHERE `id` = @id;";
            BindId(cmd);
            await cmd.ExecuteNonQueryAsync();
        }

        private void BindId(MySqlCommand cmd)
        {
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@id",
                DbType = DbType.Int32,
                Value = Id,
            });
        }

        private void BindParams(MySqlCommand cmd)
        {
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@title",
                DbType = DbType.String,
                Value = Title,
            });
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@price",
                DbType = DbType.Double,
                Value = price,
            });
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@image_url",
                DbType = DbType.String,
                Value = image_url,
            });
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@created_at",
                DbType = DbType.String,
                Value = created_at,
            });
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@updated_at",
                DbType = DbType.String,
                Value = updated_at,
            });
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@description",
                DbType = DbType.String,
                Value = description,
            });

        }
    }

}
