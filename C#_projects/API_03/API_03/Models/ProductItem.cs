using System;
using System.ComponentModel.DataAnnotations;
using System.Data;
using System.Threading.Tasks;
using MySqlConnector;
using static API_03.Models.Validation;

namespace API_03.Models
{
    public class ProductItem
    {
        
        [Required]
        public long Id { get; set; }


        [Required]
        public string Description { get; set; }


        [Required]
        [TitleAttribute]
        public string Title { get; set;}


        [Required]
        [Image_urlAttribute]
        public string Image_url { get; set; }


        [Required]
        [PriceAttribute]
        public double Price { get; set; }


        [Required]
        [DateAttribute]
        public string Created_at { get; set; }


        [Required]
        [DateAttribute]
        public string Updated_at { get; set; }


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
                Value = Price,
            });

            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@image_url",
                DbType = DbType.String,
                Value = Image_url,
            });

            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@created_at",
                DbType = DbType.String,
                Value = Created_at,
            });

            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@updated_at",
                DbType = DbType.String,
                Value = Updated_at,
            });

            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@description",
                DbType = DbType.String,
                Value = Description,
            });

        }
    }
}

