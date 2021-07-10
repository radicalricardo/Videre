--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

-- Started on 2021-07-10 01:57:28

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
-- TOC entry 3046 (class 1262 OID 107264)
-- Name: Videre; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "Videre" WITH TEMPLATE = template0 ENCODING = 'UTF8';


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
-- TOC entry 3047 (class 0 OID 0)
-- Dependencies: 3046
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
    "timestamp" timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    frame_path character varying NOT NULL
);


ALTER TABLE public.frames OWNER TO postgres;

--
-- TOC entry 3048 (class 0 OID 0)
-- Dependencies: 205
-- Name: TABLE frames; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.frames IS 'Contem cada frame guardado, quando foi guardado.';


--
-- TOC entry 3049 (class 0 OID 0)
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
-- TOC entry 3050 (class 0 OID 0)
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
    START WITH 0
    INCREMENT BY 1
    MINVALUE 0
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
    password character varying NOT NULL,
    admin boolean
);


ALTER TABLE public.utilizadores OWNER TO postgres;

--
-- TOC entry 3051 (class 0 OID 0)
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
    confianca double precision NOT NULL,
    "topLeft" integer[] NOT NULL,
    "bottomRight" integer[] NOT NULL
);


ALTER TABLE public.objects_found OWNER TO postgres;

--
-- TOC entry 3052 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE objects_found; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.objects_found IS 'Representa todos os objecto encontrados em cada frame.';


--
-- TOC entry 210 (class 1259 OID 115870)
-- Name: objects_video; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.objects_video (
    video_id integer NOT NULL,
    object_id integer NOT NULL
);


ALTER TABLE public.objects_video OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 107476)
-- Name: stream_urls; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stream_urls (
    user_id integer NOT NULL,
    stream_link character varying NOT NULL,
    videre_url character varying NOT NULL
);


ALTER TABLE public.stream_urls OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 115857)
-- Name: videos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.videos (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    frame_path character varying NOT NULL
);


ALTER TABLE public.videos OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 115855)
-- Name: videos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.videos ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.videos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 2895 (class 2606 OID 107294)
-- Name: frames Frames_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frames
    ADD CONSTRAINT "Frames_pkey" PRIMARY KEY (id);


--
-- TOC entry 2887 (class 2606 OID 107274)
-- Name: object Object_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT "Object_pkey" PRIMARY KEY (id);


--
-- TOC entry 2891 (class 2606 OID 107284)
-- Name: utilizadores User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilizadores
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- TOC entry 2897 (class 2606 OID 107451)
-- Name: objects_found objects_found_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_found
    ADD CONSTRAINT objects_found_pkey PRIMARY KEY (frame_id, object_id, "topLeft", "bottomRight");


--
-- TOC entry 2903 (class 2606 OID 115874)
-- Name: objects_video objects_video_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_video
    ADD CONSTRAINT objects_video_pkey PRIMARY KEY (video_id, object_id);


--
-- TOC entry 2899 (class 2606 OID 107483)
-- Name: stream_urls stream_urls_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stream_urls
    ADD CONSTRAINT stream_urls_pkey PRIMARY KEY (user_id, stream_link);


--
-- TOC entry 2889 (class 2606 OID 107381)
-- Name: object unique_object; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT unique_object UNIQUE (nome_objecto);


--
-- TOC entry 2893 (class 2606 OID 107421)
-- Name: utilizadores unique_username; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.utilizadores
    ADD CONSTRAINT unique_username UNIQUE (username);


--
-- TOC entry 2901 (class 2606 OID 115864)
-- Name: videos videos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.videos
    ADD CONSTRAINT videos_pkey PRIMARY KEY (id);


--
-- TOC entry 2905 (class 2606 OID 107351)
-- Name: objects_found frames_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_found
    ADD CONSTRAINT frames_fk FOREIGN KEY (frame_id) REFERENCES public.frames(id);


--
-- TOC entry 2906 (class 2606 OID 107356)
-- Name: objects_found object_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_found
    ADD CONSTRAINT object_fk FOREIGN KEY (object_id) REFERENCES public.object(id);


--
-- TOC entry 2910 (class 2606 OID 115880)
-- Name: objects_video objects_video_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_video
    ADD CONSTRAINT objects_video_object_id_fkey FOREIGN KEY (object_id) REFERENCES public.object(id);


--
-- TOC entry 2909 (class 2606 OID 115875)
-- Name: objects_video objects_video_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.objects_video
    ADD CONSTRAINT objects_video_video_id_fkey FOREIGN KEY (video_id) REFERENCES public.videos(id);


--
-- TOC entry 2904 (class 2606 OID 107295)
-- Name: frames user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.frames
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public.utilizadores(id);


--
-- TOC entry 2907 (class 2606 OID 107484)
-- Name: stream_urls user_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stream_urls
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES public.utilizadores(id);


--
-- TOC entry 2908 (class 2606 OID 115865)
-- Name: videos videos_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.videos
    ADD CONSTRAINT videos_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.utilizadores(id);


-- Completed on 2021-07-10 01:57:28

--
-- PostgreSQL database dump complete
--

