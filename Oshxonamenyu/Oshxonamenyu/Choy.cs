using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Oshxonamenyu
{
    public partial class Choy : Form
    {
        private MySqlConnection conn;
        private MySqlDataAdapter adapter;
        private DataSet ds;
        private int id_row;
        private Form1 form1;
        public Choy()
        {
            InitializeComponent();
            LoadDishes();
        }
        private void LoadDishes()
        {
            string connStr = "server=localhost;database=oshxona;uid=root;password=;";
            string query = "SELECT id, nomi, narxi, miqdori FROM choy";

            using (conn = new MySqlConnection(connStr))
            {
                using (adapter = new MySqlDataAdapter(query, conn))
                {
                    ds = new DataSet();
                    adapter.Fill(ds);
                    dataGridView1.DataSource = ds.Tables[0];
                    form1 = new Form1();
                }
            }
        }
        private void button2_Click(object sender, EventArgs e)
        {
            string connectionString = "server=localhost;database=oshxona;uid=root;password=;";

            using (MySqlConnection connection = new MySqlConnection(connectionString))
            {
                connection.Open();

                foreach (DataGridViewRow row in dataGridView1.Rows)
                {
                    if (!row.IsNewRow)
                    {
                        string nomi = row.Cells["nomi"].Value.ToString();
                        decimal narxi;
                        decimal miqdori;
                        int id;

                        if (decimal.TryParse(row.Cells["narxi"].Value.ToString(), out narxi) &&
                            decimal.TryParse(row.Cells["miqdori"].Value.ToString(), out miqdori) &&
                            int.TryParse(row.Cells["id"].Value.ToString(), out id))
                        {
                            string query = "INSERT INTO choy (id, nomi, narxi, miqdori) VALUES (@id, @nomi, @narxi, @miqdori) ON DUPLICATE KEY UPDATE nomi = @nomi, narxi = @narxi, miqdori = @miqdori";

                            using (MySqlCommand cmd = new MySqlCommand(query, connection))
                            {
                                cmd.Parameters.AddWithValue("@id", id);
                                cmd.Parameters.AddWithValue("@nomi", nomi);
                                cmd.Parameters.AddWithValue("@narxi", narxi);
                                cmd.Parameters.AddWithValue("@miqdori", miqdori);

                                cmd.ExecuteNonQuery();
                            }
                        }
                        else
                        {
                            MessageBox.Show("Xato format kiritildi!");
                        }
                    }
                }
            }

            LoadDishes();
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            id_row = e.RowIndex;
            dataGridView1.Rows[id_row].Cells["nomi"].Value.ToString();
            dataGridView1.Rows[id_row].Cells["narxi"].Value.ToString();
            dataGridView1.Rows[id_row].Cells["miqdori"].Value.ToString();
            dataGridView1.Rows[id_row].Cells["id"].Value.ToString();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            string connectionString = "server=localhost;database=oshxona;uid=root;password=;";
            if (dataGridView1.SelectedRows.Count > 0)
            {
                
                DataGridViewRow selectedRow = dataGridView1.SelectedRows[0];
               
                
                int primaryKeyValue = Convert.ToInt32(selectedRow.Cells["id"].Value);

                
                string deleteQuery = "DELETE FROM choy WHERE id = @PrimaryKeyValue";

                using (MySqlConnection connection = new MySqlConnection(connectionString))
                {
                    connection.Open();

                    using (MySqlCommand cmd = new MySqlCommand(deleteQuery, connection))
                    {
                        cmd.Parameters.AddWithValue("@PrimaryKeyValue", primaryKeyValue);
                        cmd.ExecuteNonQuery();
                    }
                }

               
                dataGridView1.Rows.Remove(selectedRow);
            }
            else
            {
                MessageBox.Show("Please select a row to delete.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

        }
    }
}
