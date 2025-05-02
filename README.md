# INFO3180 VueJS and Flask Starter

This template should help get you started developing with Vue 3 on the frontend and Flask as an API on the backend.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Start Flask API

Remember to always create a virtual environment and install the packages in your requirements file

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
$ flask --app app --debug run
```

## for clearing purposes

BEGIN;

-- Delete from child tables first (respect foreign key constraints)
DELETE FROM favourite;
DELETE FROM profile;
DELETE FROM users;

COMMIT;


INSERT INTO profile (
    id, user_id_fk, description, parish, biography, sex, race, birth_year, height,
    fav_cuisine, fav_colour, fav_school_subject, political, religious, family_oriented, created_at
) VALUES
(14, 20, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.75, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-01 10:05:23'),
(15, 20, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.85, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-02 14:12:45'),
(16, 20, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.78, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-03 09:25:12'),
(17, 21, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.90, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-04 16:08:37'),
(18, 21, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.93, 'Jamaican', 'Green', 'Chemistry', true, false, true, '2025-04-04 17:42:19'),
(19, 21, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 2.00, 'Chinese', 'Green', 'Biology', true, false, false, '2025-04-04 18:30:01'),
(20, 23, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.85, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-05 11:55:44'),
(21, 23, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.88, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-05 12:34:10'),
(22, 23, 'Test description', 'kingston', 'bio', 'Male', 'Black', 2004, 1.85, 'Jamaican', 'Red', 'Chemistry', true, false, true, '2025-04-05 13:10:29'),
(23, 22, 'Test description', 'kingston', 'bio', 'Female', 'White', 2009, 1.83, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-07 08:15:50'),
(24, 24, 'Test description', 'kingston', 'bio', 'Female', 'Black', 2005, 1.87, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-08 10:03:17'),
(25, 24, 'Test description', 'kingston', 'bio', 'Female', 'White', 2005, 1.91, 'Chinese', 'Blue', 'Math', false, false, true, '2025-04-08 11:45:00'),
(26, 26, 'Test description', 'kingston', 'bio', 'Female', 'White', 2005, 1.98, 'Jamaican', 'Blue', 'Chemistry', true, false, true, '2025-04-09 09:40:26');
