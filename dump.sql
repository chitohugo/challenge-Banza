--
-- PostgreSQL database dump
--

-- Dumped from database version 11.19 (Debian 11.19-1.pgdg110+1)
-- Dumped by pg_dump version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.clients VALUES ('Terry', 'Medhurst', 'atuny0@sohu.com', '$2b$12$TLbXhP.RImueuMP8NBsXw.Yb4Xy528Esw7bg5iA2XIiaIIWAY3PXO', 'a2995993-c078-4a58-b657-6a08ce763894', '2023-06-27 17:15:30.771485', '2023-06-27 17:15:30.771485');
INSERT INTO public.clients VALUES ('Johnathon', 'Predovic', 'johnathonp@sohu.com', '$2b$12$IrjV9Cri7eSDrE.4593/9uN9kjPKt4u5HQ47VQN4yOE.r50gMDg6u', '1cea01dd-b2f5-4774-98e1-0c54f1b3a3b1', '2023-06-27 17:17:40.208009', '2023-06-27 17:17:40.208009');
INSERT INTO public.clients VALUES ('John', 'Doe', 'johndoe@sohu.com', '$2b$12$YIIA5BdNSrZ3btpVDhAHEOyEF3QzrDnjzHatXG4qUWj07BtwvRxIm', '0c88e254-5b89-49f5-a11f-7ba94e72d442', '2023-06-27 17:18:53.589922', '2023-06-27 17:18:53.589922');
INSERT INTO public.clients VALUES ('Test', 'Test', 'test@gmail.com', '$2b$12$XZKzi11onotUEtuHS9xgre08dC5PVVellUJiTXfWXGDCQ/kdi2E72', 'b8515332-4301-423e-a9c8-bd2e39dce075', '2023-06-27 17:22:06.40585', '2023-06-27 17:22:06.40585');


--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.accounts VALUES ('0c88e254-5b89-49f5-a11f-7ba94e72d442', 'acd7299e-af60-41a7-83a4-b9b1beed2a3f', '2023-06-27 17:46:28.645064', '2023-06-27 18:09:44.808714', 48454, 630000);
INSERT INTO public.accounts VALUES ('0c88e254-5b89-49f5-a11f-7ba94e72d442', 'd3ceb63c-525c-4951-a52a-a4c47dec6998', '2023-06-27 17:46:59.793457', '2023-06-27 18:10:18.790932', 77517, 1000000);
INSERT INTO public.accounts VALUES ('b8515332-4301-423e-a9c8-bd2e39dce075', 'b28d29c3-7e8c-44cf-84f4-9425bec8d0aa', '2023-06-27 17:47:27.094934', '2023-06-30 14:05:23.142105', 75346, 1000000);
INSERT INTO public.accounts VALUES ('b8515332-4301-423e-a9c8-bd2e39dce075', '9a43b3c7-2468-4fbd-aeb4-af75e89929a2', '2023-06-29 14:52:04.747959', '2023-06-30 14:06:11.202621', 26258, 5000000);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.categories VALUES ('Category Three', '135b2969-388b-4169-b4c4-d624bc49409c', '2023-06-27 17:33:05.261961', '2023-06-27 17:33:05.261961');
INSERT INTO public.categories VALUES ('Category Two', '1715c2ce-e1cf-4795-a5c7-80d8291a5f59', '2023-06-27 17:33:11.103985', '2023-06-27 17:33:11.103985');
INSERT INTO public.categories VALUES ('Category Four', '9982f8c4-a01e-479c-bfab-4b5395362aae', '2023-06-27 17:54:36.015034', '2023-06-27 17:54:36.015034');
INSERT INTO public.categories VALUES ('Category Five', '7e567f37-4206-499b-8aa6-b87399182edd', '2023-06-29 14:49:40.521889', '2023-06-29 14:49:40.521889');
INSERT INTO public.categories VALUES ('Category One', '6f980697-90ba-4acd-ad0c-a223e4578ff0', '2023-06-26 18:42:36.487503', '2023-06-30 00:23:40.812232');


--
-- Data for Name: categories_clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.categories_clients VALUES ('b8515332-4301-423e-a9c8-bd2e39dce075', '6f980697-90ba-4acd-ad0c-a223e4578ff0', '7b7f2dff-2203-45c8-881e-623eb4a5ff51', '2023-06-27 17:37:10.108496', '2023-06-27 17:37:10.108496');
INSERT INTO public.categories_clients VALUES ('0c88e254-5b89-49f5-a11f-7ba94e72d442', '6f980697-90ba-4acd-ad0c-a223e4578ff0', '3fa85fca-0f28-43e1-89a9-12900d146776', '2023-06-27 17:37:46.104481', '2023-06-27 17:37:46.104481');
INSERT INTO public.categories_clients VALUES ('0c88e254-5b89-49f5-a11f-7ba94e72d442', '135b2969-388b-4169-b4c4-d624bc49409c', '64586477-778e-4c42-a9bb-16ef8e900683', '2023-06-27 17:38:04.639281', '2023-06-27 17:38:04.639281');


--
-- Data for Name: movements; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.movements VALUES ('acd7299e-af60-41a7-83a4-b9b1beed2a3f', 'INGRESS', 630000, 'a9e2ff35-e027-4917-b9a0-bca3f93e1f8d', '2023-06-27 18:09:44.808714', '2023-06-27 18:09:44.808714');
INSERT INTO public.movements VALUES ('d3ceb63c-525c-4951-a52a-a4c47dec6998', 'INGRESS', 1000000, 'f473458a-1cb4-4032-9ae1-0d55880783a0', '2023-06-27 18:10:18.790932', '2023-06-27 18:10:18.790932');
INSERT INTO public.movements VALUES ('b28d29c3-7e8c-44cf-84f4-9425bec8d0aa', 'INGRESS', 1000000, '6d480809-7904-4593-bf9e-ec4a8ccc69c2', '2023-06-27 18:10:51.572516', '2023-06-27 18:10:51.572516');
INSERT INTO public.movements VALUES ('b28d29c3-7e8c-44cf-84f4-9425bec8d0aa', 'INGRESS', 4000000, '562276c2-ef18-4381-b476-89ea54d579e8', '2023-06-29 14:51:41.282986', '2023-06-29 14:51:41.282986');
INSERT INTO public.movements VALUES ('b28d29c3-7e8c-44cf-84f4-9425bec8d0aa', 'EGRESS', 4000000, 'b8004b44-f61f-4ac4-bb7c-3964146d9983', '2023-06-30 14:04:27.612281', '2023-06-30 14:04:27.612281');
INSERT INTO public.movements VALUES ('b28d29c3-7e8c-44cf-84f4-9425bec8d0aa', 'INGRESS', 1000000, '7dab5e63-5a45-4f47-90a1-e75f8a11a57b', '2023-06-30 14:04:58.908499', '2023-06-30 14:04:58.908499');
INSERT INTO public.movements VALUES ('b28d29c3-7e8c-44cf-84f4-9425bec8d0aa', 'EGRESS', 1000000, '151edd05-4ae3-4bee-93c1-3c4507df8f5d', '2023-06-30 14:05:23.142105', '2023-06-30 14:05:23.142105');
INSERT INTO public.movements VALUES ('9a43b3c7-2468-4fbd-aeb4-af75e89929a2', 'INGRESS', 5000000, '4b9419c6-221f-4b55-9b35-a18da8aed9d3', '2023-06-30 14:06:11.202621', '2023-06-30 14:06:11.202621');


--
-- PostgreSQL database dump complete
--

