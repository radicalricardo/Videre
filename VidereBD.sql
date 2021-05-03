--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

-- Started on 2021-05-03 18:46:49

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
-- TOC entry 3016 (class 1262 OID 107264)
-- Name: Videre; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "Videre" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Portuguese_Brazil.1252';


ALTER DATABASE "Videre" OWNER TO postgres;

\connect "Videre"

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
-- TOC entry 3017 (class 0 OID 0)
-- Dependencies: 3016
-- Name: DATABASE "Videre"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE "Videre" IS 'Base de dados relativa ao projecto videre (interface web com yolo e openCV). Projeto de fim de curso na UAL em parceria com a Leitek Innovative Solutions.';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 205 (class 1259 OID 107287)
-- Name: frames; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.frames (
    id integer NOT NULL,
    frame bytea NOT NULL,
    "timestamp" timestamp with time zone,
    user_id integer NOT NULL
);


ALTER TABLE public.frames OWNER TO postgres;

--
-- TOC entry 3018 (class 0 OID 0)
-- Dependencies: 205
-- Name: TABLE frames; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.frames IS 'Contem cada frame guardado, quando foi guardado, o objecto detetado, objecto detetado, e coordenadas do objecto.';


--
-- TOC entry 3019 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN frames.frame; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.frames.frame IS 'Representa a imagem deteta. Placeholder.';


--
-- TOC entry 3020 (class 0 OID 0)
-- Dependencies: 205
-- Name: COLUMN frames.user_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.frames.user_id IS 'id do utilizador';


--
-- TOC entry 204 (class 1259 OID 107285)
-- Name: Frames_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.frames ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Frames_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    CYCLE
);


--
-- TOC entry 201 (class 1259 OID 107267)
-- Name: object; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.object (
    nome_objecto character varying NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.object OWNER TO postgres;

--
-- TOC entry 3021 (class 0 OID 0)
-- Dependencies: 201
-- Name: TABLE object; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.object IS 'Identifica univocamente cada objecto dentro da base de dados.';


--
-- TOC entry 200 (class 1259 OID 107265)
-- Name: Object_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.object ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Object_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    CYCLE
);


--
-- TOC entry 203 (class 1259 OID 107277)
-- Name: utilizadores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.utilizadores (
    id integer NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.utilizadores OWNER TO postgres;

--
-- TOC entry 3022 (class 0 OID 0)
-- Dependencies: 203
-- Name: TABLE utilizadores; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.utilizadores IS 'Representa os utilizadores do sistema.
Placeholder.';


--
-- TOC entry 202 (class 1259 OID 107275)
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.utilizadores ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."User_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
    CYCLE
);


--
-- TOC entry 206 (class 1259 OID 107346)
-- Name: objects_found; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.objects_found (
    frame_id integer NOT NULL,
    object_id integer NOT NULL,
    coord_box integer[] NOT NULL
);


ALTER TABLE public.objects_found OWNER TO postgres;

--
-- TOC entry 3023 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE objects_found; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.objects_found IS 'Representa todos os objecto encontrados em cada frame.';


--
-- TOC entry 2875 (class 2606 OID 107294)
-- Name: frames Frames_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frames
    ADD CONSTRAINT "Frames_pkey" PRIMARY KEY (id);


--
-- TOC entry 2871 (class 2606 OID 107274)
-- Name: object Object_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT "Object_pkey" PRIMARY KEY (id);


--
-- TOC entry 2877 (class 2606 OID 107365)
-- Name: objects_found Objects_Found_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_found
    ADD CONSTRAINT "Objects_Found_pkey" PRIMARY KEY (frame_id, object_id, coord_box);


--
-- TOC entry 2873 (class 2606 OID 107284)
-- Name: utilizadores User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilizadores
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- TOC entry 2879 (class 2606 OID 107351)
-- Name: objects_found frames_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_found
    ADD CONSTRAINT frames_fk FOREIGN KEY (frame_id) REFERENCES public.frames(id);


--
-- TOC entry 2880 (class 2606 OID 107356)
-- Name: objects_found object_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_found
    ADD CONSTRAINT object_fk FOREIGN KEY (object_id) REFERENCES public.object(id);


--
-- TOC entry 2878 (class 2606 OID 107295)
-- Name: frames user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frames
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public.utilizadores(id);


-- Completed on 2021-05-03 18:46:51

--
-- PostgreSQL database dump complete
--

